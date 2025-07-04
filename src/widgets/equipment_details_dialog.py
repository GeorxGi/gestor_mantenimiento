import flet as ft
from src.consts.colors import *
from src.models.equipment import Equipment

def equipment_details_dialog(page: ft.Page, equipment: Equipment):
    
    # Icono principal del equipo
    equipment_icon = ft.Container(
        width=120,
        height=120,
        bgcolor=ft.Colors.GREY_100,
        border_radius=20,
        border=ft.border.all(2, ft.Colors.GREY_300),
        alignment=ft.alignment.center,
        content=ft.Icon(
            ft.Icons.PRECISION_MANUFACTURING,
            size=60,
            color=purple_color
        )
    )
    
    # Información del equipo con mejor diseño
    info_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.TAG, color=purple_color, size=20),
                    ft.Text(f"#{equipment.code}", size=16, weight=ft.FontWeight.BOLD, color=purple_color)
                ], spacing=8),
                ft.Row([
                    ft.Icon(ft.Icons.INVENTORY, color=dark_grey_color, size=20),
                    ft.Text(equipment.name, size=16, weight=ft.FontWeight.W_500)
                ], spacing=8),
                ft.Row([
                    ft.Icon(ft.Icons.DESCRIPTION, color=middle_color, size=20),
                    ft.Text(equipment.description, size=14, color=dark_grey_color, expand=True)
                ], spacing=8),
                ft.Row([
                    ft.Icon(ft.Icons.BUSINESS, color=grey_color, size=20),
                    ft.Text(f"Proveedor: {equipment.provider}", size=14, color=grey_color)
                ], spacing=8)
            ], spacing=12),
            padding=20,
            width=400
        ),
        elevation=2
    )
    
    # Botones de acción
    action_buttons = ft.Row([
        ft.ElevatedButton(
            text="Editar",
            icon=ft.Icons.EDIT,
            bgcolor=middle_color,
            color=ft.Colors.WHITE,
            on_click=lambda _: edit_equipment(page, dialog, equipment)
        ),
        ft.ElevatedButton(
            text="Eliminar",
            icon=ft.Icons.DELETE,
            bgcolor=ft.Colors.RED_400,
            color=ft.Colors.WHITE,
            on_click=lambda _: delete_equipment_confirm(page, dialog, equipment)
        ),
        ft.OutlinedButton(
            text="Cerrar",
            on_click=lambda _: page.close(dialog)
        )
    ], spacing=10, alignment=ft.MainAxisAlignment.CENTER)
    
    dialog = ft.AlertDialog(
        title=ft.Row([
            ft.Icon(ft.Icons.PRECISION_MANUFACTURING, color=purple_color),
            ft.Text("Detalles del Equipo", size=20, weight=ft.FontWeight.BOLD)
        ], spacing=10),
        content=ft.Column([
            equipment_icon,
            ft.Divider(height=20),
            info_card,
            ft.Divider(height=10),
            action_buttons
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
        content_padding=30
    )
    page.open(dialog)

def edit_equipment(page: ft.Page, current_dialog, equipment: Equipment):
    name_field = ft.Container(
        content=ft.TextField(
            value=equipment.name,
            label="Nombre del equipo",
            prefix_icon=ft.Icons.INVENTORY,
            border_radius=15,
            border_color=middle_color,
            focused_border_color=purple_color,
            label_style=ft.TextStyle(color=middle_color),
            text_style=ft.TextStyle(size=16, weight=ft.FontWeight.W_500),
            content_padding=ft.padding.symmetric(horizontal=15, vertical=12)
        ),
        width=380,
        padding=ft.padding.all(5)
    )
    description_field = ft.Container(
        content=ft.TextField(
            value=equipment.description,
            label="Descripción",
            prefix_icon=ft.Icons.DESCRIPTION,
            multiline=True,
            max_lines=3,
            border_radius=15,
            border_color=middle_color,
            focused_border_color=purple_color,
            label_style=ft.TextStyle(color=middle_color),
            text_style=ft.TextStyle(size=14),
            content_padding=ft.padding.symmetric(horizontal=15, vertical=12)
        ),
        width=380,
        padding=ft.padding.all(5)
    )
    provider_field = ft.Container(
        content=ft.TextField(
            value=equipment.provider,
            label="Proveedor",
            prefix_icon=ft.Icons.BUSINESS,
            border_radius=15,
            border_color=middle_color,
            focused_border_color=purple_color,
            label_style=ft.TextStyle(color=middle_color),
            text_style=ft.TextStyle(size=16),
            content_padding=ft.padding.symmetric(horizontal=15, vertical=12)
        ),
        width=380,
        padding=ft.padding.all(5)
    )
    
    def save_changes(e):
        # Aquí iría la lógica para actualizar el equipo
        page.close(edit_dialog)
        page.close(current_dialog)
        page.snack_bar = ft.SnackBar(content=ft.Text("Equipo actualizado correctamente"))
        page.snack_bar.open = True
        page.update()
    
    edit_dialog = ft.AlertDialog(
        title=ft.Row([
            ft.Icon(ft.Icons.EDIT, color=middle_color),
            ft.Text("Editar Equipo", weight=ft.FontWeight.BOLD)
        ], spacing=10),
        content=ft.Column([name_field, description_field, provider_field], spacing=15, tight=True),
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

def delete_equipment_confirm(page: ft.Page, current_dialog, equipment: Equipment):
    def confirm_delete(e):
        # Aquí iría la lógica para eliminar el equipo
        page.close(confirm_dialog)
        page.close(current_dialog)
        page.snack_bar = ft.SnackBar(content=ft.Text("Equipo eliminado correctamente"))
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
                f"¿Estás seguro de que quieres eliminar el equipo '{equipment.name}'?",
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