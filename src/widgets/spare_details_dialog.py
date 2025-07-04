import flet as ft
from src.consts.colors import *
import os
from src.consts.file_dir import SPARE_IMAGES_PATH

def spare_details_window(*, page: ft.Page, code:int, name:str, quantity:int, image_src:str = None, on_update=None, on_delete=None):
    
    # Obtener nivel de acceso del usuario
    from src.enums.access_level import AccessLevel
    user_data = page.session.get("local_user")
    user_access_level = None
    if user_data:
        try:
            user_access_level = AccessLevel.from_string(user_data.get("access_level", "USER"))
        except:
            user_access_level = AccessLevel.USER
    else:
        user_access_level = AccessLevel.USER
    
    # Imagen principal más grande y bonita
    container_img = ft.Container(
        width=200,
        height=200,
        bgcolor=ft.Colors.GREY_100,
        border_radius=20,
        border=ft.border.all(2, ft.Colors.GREY_300),
        alignment=ft.alignment.center,
        content=ft.Image(
            src=image_src,
            fit=ft.ImageFit.COVER,
            border_radius=ft.border_radius.all(18)) if image_src else ft.Icon(
            ft.Icons.IMAGE_OUTLINED,
            size=80,
            color=ft.Colors.GREY_400
        )
    )
    
    # Botón para cambiar imagen
    change_image_btn = ft.IconButton(
        icon=ft.Icons.CAMERA_ALT,
        bgcolor=purple_color,
        icon_color=ft.Colors.WHITE,
        tooltip="Cambiar imagen",
        on_click=lambda _: change_image(page, code, container_img, on_update)
    )
    
    # Contenedor de imagen con botón
    image_section = ft.Column([
        container_img,
        ft.Container(
            content=change_image_btn,
            alignment=ft.alignment.center,
            margin=ft.margin.only(top=-10)
        )
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
    
    # Información de la pieza con mejor diseño
    info_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.TAG, color=purple_color, size=20),
                    ft.Text(f"#{code}", size=16, weight=ft.FontWeight.BOLD, color=purple_color)
                ], spacing=8),
                ft.Row([
                    ft.Icon(ft.Icons.INVENTORY, color=dark_grey_color, size=20),
                    ft.Text(name, size=16, weight=ft.FontWeight.W_500)
                ], spacing=8),
                ft.Row([
                    ft.Icon(ft.Icons.NUMBERS, color=middle_color, size=20),
                    ft.Text(f"{quantity} unidades", size=16, color=dark_grey_color)
                ], spacing=8)
            ], spacing=12),
            padding=20,
            width=300
        ),
        elevation=2
    )
    
    # Botones de acción según el rol del usuario
    action_buttons_list = []
    
    # Botones comunes para supervisores y admins
    if user_access_level in [AccessLevel.SUPERVISOR, AccessLevel.ADMIN]:
        action_buttons_list.extend([
            ft.ElevatedButton(
                text="Editar",
                icon=ft.Icons.EDIT,
                bgcolor=middle_color,
                color=ft.Colors.WHITE,
                on_click=lambda _: edit_spare(page, dialog, code, name, quantity, on_update)
            ),
            ft.ElevatedButton(
                text="Eliminar",
                icon=ft.Icons.DELETE,
                bgcolor=ft.Colors.RED_400,
                color=ft.Colors.WHITE,
                on_click=lambda _: delete_spare_confirm(page, dialog, code, on_delete)
            )
        ])
    
    # Botón específico para supervisores
    if user_access_level == AccessLevel.SUPERVISOR:
        action_buttons_list.append(
            ft.ElevatedButton(
                text="Solicitar Reposición",
                icon=ft.Icons.REQUEST_QUOTE,
                bgcolor=ft.Colors.ORANGE,
                color=ft.Colors.WHITE,
                on_click=lambda _: request_restock(page, dialog, code, name, quantity)
            )
        )
    
    # Botón específico para admins
    if user_access_level == AccessLevel.ADMIN:
        action_buttons_list.append(
            ft.ElevatedButton(
                text="Reponer Pieza",
                icon=ft.Icons.ADD_BOX,
                bgcolor=ft.Colors.GREEN,
                color=ft.Colors.WHITE,
                on_click=lambda _: restock_spare(page, dialog, code, name, quantity, on_update)
            )
        )
    
    # Botón cerrar siempre presente
    action_buttons_list.append(
        ft.OutlinedButton(
            text="Cerrar",
            on_click=lambda _: page.close(dialog)
        )
    )
    
    action_buttons = ft.Row(
        action_buttons_list,
        spacing=8, 
        alignment=ft.MainAxisAlignment.CENTER,
        wrap=True
    )
    
    dialog = ft.AlertDialog(
        title=ft.Row([
            ft.Icon(ft.Icons.SETTINGS, color=purple_color),
            ft.Text("Detalles de la Pieza", size=20, weight=ft.FontWeight.BOLD)
        ], spacing=10),
        content=ft.Column([
            image_section,
            ft.Divider(height=20),
            info_card,
            ft.Divider(height=10),
            action_buttons
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
        content_padding=30
    )
    page.open(dialog)

def change_image(page: ft.Page, code: int, image_container, on_update):
    file_picker = ft.FilePicker(
        on_result=lambda e: handle_image_selection(e, page, code, image_container, on_update)
    )
    page.overlay.append(file_picker)
    page.update()
    file_picker.pick_files(allowed_extensions=["jpg", "jpeg", "png"])

def handle_image_selection(e, page: ft.Page, code: int, image_container, on_update):
    if e.files:
        file_path = e.files[0].path
        # Procesar y guardar la nueva imagen
        from src.controllers.spare_controller import process_and_store_image
        import shutil
        
        try:
            with open(file_path, 'rb') as f:
                image_bytes = f.read()
            
            output_path = os.path.join(SPARE_IMAGES_PATH, f"{code}.jpg")
            if process_and_store_image(image_bytes, output_path):
                # Actualizar la imagen en el contenedor
                image_container.content = ft.Image(
                    src=output_path,
                    fit=ft.ImageFit.COVER,
                    border_radius=ft.border_radius.all(18)
                )
                page.update()
                if on_update:
                    on_update()
                page.snack_bar = ft.SnackBar(content=ft.Text("Imagen actualizada"))
                page.snack_bar.open = True
                page.update()
            else:
                page.snack_bar = ft.SnackBar(content=ft.Text("Error al procesar imagen"))
            page.snack_bar.open = True
            page.update()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Error: {str(ex)}"))
            page.snack_bar.open = True
            page.update()

def edit_spare(page: ft.Page, current_dialog, code: int, name: str, quantity: int, on_update):
    name_field = ft.Container(
        content=ft.TextField(
            value=name, 
            label="Nombre de la pieza",
            prefix_icon=ft.Icons.INVENTORY,
            border_radius=15,
            border_color=middle_color,
            focused_border_color=purple_color,
            label_style=ft.TextStyle(color=middle_color),
            text_style=ft.TextStyle(size=16),
            content_padding=ft.padding.symmetric(horizontal=15, vertical=12)
        ),
        width=320,
        padding=ft.padding.all(5)
    )
    quantity_field = ft.Container(
        content=ft.TextField(
            value=str(quantity), 
            label="Cantidad", 
            keyboard_type=ft.KeyboardType.NUMBER,
            prefix_icon=ft.Icons.NUMBERS,
            border_radius=15,
            border_color=middle_color,
            focused_border_color=purple_color,
            label_style=ft.TextStyle(color=middle_color),
            text_style=ft.TextStyle(size=16),
            content_padding=ft.padding.symmetric(horizontal=15, vertical=12)
        ),
        width=320,
        padding=ft.padding.all(5)
    )
    
    def save_changes(e):
        from src.controllers.spare_controller import update_spare
        try:
            new_quantity = int(quantity_field.content.value)
            if update_spare(code, name_field.content.value, new_quantity):
                page.close(edit_dialog)
                page.close(current_dialog)
                if on_update:
                    on_update()
                page.snack_bar = ft.SnackBar(content=ft.Text("Pieza actualizada correctamente"))
                page.snack_bar.open = True
                page.update()
            else:
                page.snack_bar = ft.SnackBar(content=ft.Text("Error al actualizar la pieza"))
                page.snack_bar.open = True
                page.update()
        except ValueError:
            page.snack_bar = ft.SnackBar(content=ft.Text("La cantidad debe ser un número"))
            page.snack_bar.open = True
            page.update()
    
    edit_dialog = ft.AlertDialog(
        title=ft.Row([
            ft.Icon(ft.Icons.EDIT, color=middle_color),
            ft.Text("Editar Pieza", weight=ft.FontWeight.BOLD)
        ], spacing=10),
        content=ft.Column([name_field, quantity_field], spacing=15, tight=True),
        actions=[
            ft.ElevatedButton(
                text="Guardar", 
                icon=ft.Icons.SAVE,
                bgcolor=middle_color,
                color=ft.Colors.WHITE,
                on_click=save_changes
            ),
            ft.OutlinedButton(
                text="Cancelar", 
                on_click=lambda _: page.close(edit_dialog)
            )
        ]
    )
    page.open(edit_dialog)

def delete_spare_confirm(page: ft.Page, current_dialog, code: int, on_delete):
    def confirm_delete(e):
        from src.controllers.spare_controller import delete_spare
        if delete_spare(code):
            page.close(confirm_dialog)
            page.close(current_dialog)
            if on_delete:
                on_delete()
            page.snack_bar = ft.SnackBar(content=ft.Text("Pieza eliminada correctamente"))
            page.snack_bar.open = True
            page.update()
        else:
            page.snack_bar = ft.SnackBar(content=ft.Text("Error al eliminar la pieza"))
            page.snack_bar.open = True
            page.update()
    
    confirm_dialog = ft.AlertDialog(
        title=ft.Row([
            ft.Icon(ft.Icons.WARNING, color=ft.Colors.RED_400),
            ft.Text("Confirmar Eliminación", weight=ft.FontWeight.BOLD)
        ], spacing=10),
        content=ft.Column([
            ft.Icon(ft.Icons.DELETE_FOREVER, size=60, color=ft.Colors.RED_300),
            ft.Text(
                "¿Estás seguro de que quieres eliminar esta pieza?", 
                text_align=ft.TextAlign.CENTER,
                size=16
            ),
            ft.Text(
                "Esta acción no se puede deshacer.", 
                text_align=ft.TextAlign.CENTER,
                color=ft.Colors.GREY_600,
                size=12
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10, tight=True),
        actions=[
            ft.ElevatedButton(
                text="Eliminar", 
                icon=ft.Icons.DELETE,
                bgcolor=ft.Colors.RED_400,
                color=ft.Colors.WHITE,
                on_click=confirm_delete
            ),
            ft.OutlinedButton(
                text="Cancelar", 
                on_click=lambda _: page.close(confirm_dialog)
            )
        ]
    )
    page.open(confirm_dialog)

def request_restock(page: ft.Page, current_dialog, code: int, name: str, current_quantity: int):
    """Función para que supervisores soliciten reposición de piezas"""
    quantity_field = ft.Container(
        content=ft.TextField(
            label="Cantidad a solicitar",
            keyboard_type=ft.KeyboardType.NUMBER,
            prefix_icon=ft.Icons.REQUEST_QUOTE,
            border_radius=15,
            border_color=ft.Colors.ORANGE_300,
            focused_border_color=ft.Colors.ORANGE,
            label_style=ft.TextStyle(color=ft.Colors.ORANGE_600),
            text_style=ft.TextStyle(size=16),
            content_padding=ft.padding.symmetric(horizontal=15, vertical=12)
        ),
        width=350,
        padding=ft.padding.all(5)
    )
    reason_field = ft.Container(
        content=ft.TextField(
            label="Motivo de la solicitud",
            multiline=True,
            max_lines=3,
            prefix_icon=ft.Icons.DESCRIPTION,
            border_radius=15,
            border_color=ft.Colors.ORANGE_300,
            focused_border_color=ft.Colors.ORANGE,
            label_style=ft.TextStyle(color=ft.Colors.ORANGE_600),
            text_style=ft.TextStyle(size=14),
            content_padding=ft.padding.symmetric(horizontal=15, vertical=12)
        ),
        width=350,
        padding=ft.padding.all(5)
    )
    
    def send_request(e):
        try:
            requested_qty = int(quantity_field.content.value or 0)
            if requested_qty <= 0:
                page.snack_bar = ft.SnackBar(content=ft.Text("Ingrese una cantidad válida"))
                page.snack_bar.open = True
                page.update()
                return
            
            # Aquí iría la lógica para enviar la solicitud de reposición
            page.close(request_dialog)
            page.close(current_dialog)
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Solicitud de reposición de {requested_qty} unidades de {name} enviada"))
            page.snack_bar.open = True
            page.update()
            
        except ValueError:
            page.snack_bar = ft.SnackBar(content=ft.Text("Ingrese un número válido"))
            page.snack_bar.open = True
            page.update()
    
    request_dialog = ft.AlertDialog(
        title=ft.Row([
            ft.Icon(ft.Icons.REQUEST_QUOTE, color=ft.Colors.ORANGE),
            ft.Text("Solicitar Reposición", weight=ft.FontWeight.BOLD)
        ], spacing=10),
        content=ft.Column([
            ft.Text(f"Pieza: {name} (Stock actual: {current_quantity})", weight=ft.FontWeight.W_500),
            ft.Divider(height=10),
            quantity_field,
            reason_field
        ], spacing=15, tight=True),
        actions=[
            ft.ElevatedButton(
                text="Enviar Solicitud",
                icon=ft.Icons.SEND,
                bgcolor=ft.Colors.ORANGE,
                color=ft.Colors.WHITE,
                on_click=send_request
            ),
            ft.OutlinedButton(
                text="Cancelar",
                on_click=lambda _: page.close(request_dialog)
            )
        ]
    )
    page.open(request_dialog)

def restock_spare(page: ft.Page, current_dialog, code: int, name: str, current_quantity: int, on_update):
    """Función para que admins repongan piezas directamente"""
    quantity_field = ft.Container(
        content=ft.TextField(
            label="Cantidad a reponer",
            keyboard_type=ft.KeyboardType.NUMBER,
            prefix_icon=ft.Icons.ADD_BOX,
            border_radius=15,
            border_color=ft.Colors.GREEN_300,
            focused_border_color=ft.Colors.GREEN,
            label_style=ft.TextStyle(color=ft.Colors.GREEN_600),
            text_style=ft.TextStyle(size=16, weight=ft.FontWeight.W_500),
            content_padding=ft.padding.symmetric(horizontal=15, vertical=12)
        ),
        width=320,
        padding=ft.padding.all(5)
    )
    
    def add_stock(e):
        try:
            restock_qty = int(quantity_field.content.value or 0)
            if restock_qty <= 0:
                page.snack_bar = ft.SnackBar(content=ft.Text("Ingrese una cantidad válida"))
                page.snack_bar.open = True
                page.update()
                return
            
            # Actualizar el stock sumando la cantidad
            from src.controllers.spare_controller import update_spare
            new_quantity = current_quantity + restock_qty
            
            if update_spare(code, name, new_quantity):
                page.close(restock_dialog)
                page.close(current_dialog)
                if on_update:
                    on_update()
                page.snack_bar = ft.SnackBar(content=ft.Text(f"Se agregaron {restock_qty} unidades. Stock actual: {new_quantity}"))
                page.snack_bar.open = True
                page.update()
            else:
                page.snack_bar = ft.SnackBar(content=ft.Text("Error al reponer el stock"))
                page.snack_bar.open = True
                page.update()
            
        except ValueError:
            page.snack_bar = ft.SnackBar(content=ft.Text("Ingrese un número válido"))
            page.snack_bar.open = True
            page.update()
    
    restock_dialog = ft.AlertDialog(
        title=ft.Row([
            ft.Icon(ft.Icons.ADD_BOX, color=ft.Colors.GREEN),
            ft.Text("Reponer Pieza", weight=ft.FontWeight.BOLD)
        ], spacing=10),
        content=ft.Column([
            ft.Text(f"Pieza: {name} (Stock actual: {current_quantity})", weight=ft.FontWeight.W_500),
            ft.Divider(height=10),
            quantity_field,
            ft.Text(
                "El stock se sumará al existente",
                size=12,
                color=ft.Colors.GREY_600,
                italic=True
            )
        ], spacing=15, tight=True),
        actions=[
            ft.ElevatedButton(
                text="Reponer Stock",
                icon=ft.Icons.ADD,
                bgcolor=ft.Colors.GREEN,
                color=ft.Colors.WHITE,
                on_click=add_stock
            ),
            ft.OutlinedButton(
                text="Cancelar",
                on_click=lambda _: page.close(restock_dialog)
            )
        ]
    )
    page.open(restock_dialog)