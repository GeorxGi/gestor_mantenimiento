import flet as ft 
from src.consts.colors import *
from src.widgets.spare_card import spare_card
from src.widgets.spare_details_dialog import spare_details_window
from src.enums.access_level import AccessLevel
from src.widgets.equipment_details_dialog import equipment_details_dialog
from src.widgets.maintenance_details_dialog import maintenance_details_dialog
from src.models.equipment import Equipment
from src.widgets.filter_dialog import filter_dialog
from src.controllers.equipment_controller import get_all_equipments, get_equipment_by_partial_name
from src.controllers.maintenance_controller import get_all_maintenance_orders, get_supervisor_pending_maintenances, conclude_maintenance, get_technician_names_for_maintenance
from src.controllers.spare_controller import get_all_spares
from src.consts.file_dir import SPARE_IMAGES_PATH
import os

def inventory(page: ft.Page):
    
    # Obtener nivel de acceso del usuario
    user_data = page.session.get("local_user")
    user_access_level = None
    if user_data:
        try:
            user_access_level = AccessLevel.from_string(user_data.get("access_level", "USER"))
        except:
            user_access_level = AccessLevel.USER
    else:
        user_access_level = AccessLevel.USER
    
    show_pieces = ft.Ref[bool]()
    show_equipment = ft.Ref[bool]()
    show_maintenance = ft.Ref[bool]()
    show_pieces.current = True
    show_equipment.current = False
    show_maintenance.current = False
    
    def update_filters(pieces, equipment, maintenance):
        show_pieces.current = pieces
        show_equipment.current = equipment
        show_maintenance.current = maintenance
        update_cards()
    
    def open_filter_dialog(e):
        filter_dialog(page, update_filters)
    
    search_bar = ft.Row(
        [
           ft.TextField(hint_text="buscar por nombre...",
                        prefix_icon=ft.Icons.SEARCH,
                        width=300,
                        border_radius= ft.border_radius.all(30),
                        border_color=ft.Colors.GREY_300),
            ft.IconButton(
                bgcolor= middle_color,
                icon_color=ft.Colors.WHITE,
                icon= ft.Icons.FILTER_LIST,
                on_click=open_filter_dialog
            ),
        ],
        alignment= ft.MainAxisAlignment.CENTER,
        vertical_alignment= ft.CrossAxisAlignment.CENTER,
        spacing= 10
    )
    
    # Obtener piezas de la base de datos
    spare_data = get_all_spares()
    
    # Obtener equipos de la base de datos
    equipment_objects = get_equipment_by_partial_name("")
    equipment_data = [
        {
            "code": eq.code,
            "name": eq.name,
            "description": eq.description,
            "provider": eq.provider
        }
        for eq in equipment_objects
    ]
    
    # Obtener órdenes de mantenimiento de la base de datos
    maintenance_objects = get_all_maintenance_orders()
    maintenance_data = []
    for maint in maintenance_objects:
        technician_names = get_technician_names_for_maintenance(maint.id)
        
        # Manejo robusto de fechas con debug
        date_str = "Fecha no disponible"
        if maint.maintenance_date:
            try:
                date_str = maint.maintenance_date.strftime("%d/%m/%Y")
            except Exception as e:
                # Debug: mostrar el valor real y el error
                date_str = f"Debug: {str(maint.maintenance_date)} - Error: {str(e)}"
        else:
            # Debug: mostrar que la fecha es None
            date_str = f"Debug: maintenance_date es None o vacío"
        maintenance_data.append({
            "id": maint.id,
            "equipment_code": maint.equipment_code,
            "details": maint.details,
            "date": date_str,
            "status": "Pendiente" if maint.is_pending else "Completado",
            "technicians": ", ".join(technician_names) if technician_names else "Sin asignar"
        })
    
    def create_content():
        if show_pieces.current:
            # Crear filas de 2 cards para piezas
            cards = []
            for item in spare_data:
                # Verificar si existe imagen para esta pieza
                image_path = os.path.join(SPARE_IMAGES_PATH, f"{item['code']}.jpg")
                image_src = str(image_path) if os.path.exists(image_path) else None
                
                # Determinar qué diálogo mostrar según el nivel de acceso
                if user_access_level == AccessLevel.TECHNICIAN:
                    on_click_handler = lambda e, item=item, img_src=image_src: technician_spare_details(
                        page=page, code=item["code"], name=item["name"], quantity=item["amount"], image_src=img_src
                    )
                else:
                    on_click_handler = lambda e, item=item, img_src=image_src: spare_details_window(
                        page=page, code=item["code"], name=item["name"], quantity=item["amount"], image_src=img_src,
                        on_update=update_cards, on_delete=update_cards
                    )
                
                card = spare_card(
                    code=item["code"],
                    name=item["name"],
                    image_src=image_src,
                    on_click=on_click_handler
                )
                cards.append(card)
            
            card_rows = []
            for i in range(0, len(cards), 2):
                row_cards = []
                for j in range(2):
                    if i + j < len(cards):
                        row_cards.append(cards[i + j])
                
                card_rows.append(
                    ft.Row(
                        controls=row_cards,
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20
                    )
                )
            return card_rows
        
        elif show_equipment.current:
            # Crear cards bonitas para equipos
            equipment_cards = []
            if equipment_data:
                for item in equipment_data:
                    equipment_card = ft.Card(
                        content=ft.Container(
                            content=ft.Row([
                                ft.Container(
                                    content=ft.Icon(
                                        ft.Icons.PRECISION_MANUFACTURING, 
                                        size=40, 
                                        color=purple_color
                                    ),
                                    bgcolor=ft.Colors.GREY_100,
                                    border_radius=15,
                                    padding=15,
                                    width=70,
                                    height=70,
                                    alignment=ft.alignment.center
                                ),
                                ft.Column([
                                    ft.Text(
                                        item["name"], 
                                        size=16, 
                                        weight=ft.FontWeight.BOLD, 
                                        color=dark_grey_color
                                    ),
                                    ft.Text(
                                        f"Código: #{item['code']}", 
                                        size=14, 
                                        color=purple_color,
                                        weight=ft.FontWeight.W_500
                                    ),
                                    ft.Text(
                                        item["description"][:50] + "..." if len(item["description"]) > 50 else item["description"], 
                                        size=12, 
                                        color=grey_color
                                    )
                                ], spacing=4, alignment=ft.MainAxisAlignment.CENTER, expand=True),
                                ft.Container(
                                    content=ft.Icon(
                                        ft.Icons.ARROW_FORWARD_IOS, 
                                        size=16, 
                                        color=middle_color
                                    ),
                                    padding=10
                                )
                            ], spacing=15),
                            padding=20,
                            on_click=lambda e, item=item: (
                                technician_equipment_details(page, Equipment(code=item["code"], name=item["name"], description=item["description"], provider=item["provider"]))
                                if user_access_level == AccessLevel.TECHNICIAN
                                else equipment_details_dialog(page, Equipment(code=item["code"], name=item["name"], description=item["description"], provider=item["provider"]))
                            )
                        ),
                        elevation=2,
                        margin=ft.margin.symmetric(vertical=5)
                    )
                    equipment_cards.append(equipment_card)
            else:
                equipment_cards.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.INVENTORY_2_OUTLINED, size=60, color=ft.Colors.GREY_400),
                            ft.Text("No hay equipos registrados", size=16, color=ft.Colors.GREY_500)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                        padding=40,
                        alignment=ft.alignment.center
                    )
                )
            
            return [ft.Column(controls=equipment_cards, spacing=10)]
        
        elif show_maintenance.current:
            # Verificar si el usuario es técnico
            if user_access_level == AccessLevel.TECHNICIAN:
                # Los técnicos no pueden ver las órdenes de mantenimiento
                return [ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.LOCK, size=80, color=ft.Colors.GREY_400),
                        ft.Text(
                            "Acceso Restringido", 
                            size=20, 
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREY_600
                        ),
                        ft.Text(
                            "No tienes permisos para ver las órdenes de mantenimiento.", 
                            size=14, 
                            color=ft.Colors.GREY_500,
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Text(
                            "Contacta a tu supervisor para más información.", 
                            size=12, 
                            color=ft.Colors.GREY_400,
                            text_align=ft.TextAlign.CENTER
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
                    padding=60,
                    alignment=ft.alignment.center
                )]
            
            # Para supervisores y admins - funcionalidad completa
            maintenance_cards = []
            if maintenance_data:
                for item in maintenance_data:
                    status_color = ft.Colors.ORANGE if item["status"] == "Pendiente" else ft.Colors.GREEN
                    status_icon = ft.Icons.SCHEDULE if item["status"] == "Pendiente" else ft.Icons.CHECK_CIRCLE
                    
                    maintenance_card = ft.Card(
                        content=ft.Container(
                            content=ft.Row([
                                ft.Container(
                                    content=ft.Icon(
                                        status_icon,
                                        size=40,
                                        color=status_color
                                    ),
                                    bgcolor=ft.Colors.GREY_100,
                                    border_radius=15,
                                    padding=15,
                                    width=70,
                                    height=70,
                                    alignment=ft.alignment.center
                                ),
                                ft.Column([
                                    ft.Text(
                                        f"Equipo: {item['equipment_code']}",
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                        color=dark_grey_color
                                    ),
                                    ft.Text(
                                        f"Técnicos: {item['technicians']}",
                                        size=14,
                                        color=purple_color,
                                        weight=ft.FontWeight.W_500
                                    ),
                                    ft.Text(
                                        item["details"][:50] + "..." if len(item["details"]) > 50 else item["details"],
                                        size=12,
                                        color=grey_color
                                    ),
                                    ft.Text(
                                        f"Fecha: {item['date']}",
                                        size=11,
                                        color=ft.Colors.GREY_600
                                    ),
                                    ft.Text(
                                        item["status"],
                                        size=12,
                                        color=status_color,
                                        weight=ft.FontWeight.BOLD
                                    )
                                ], spacing=3, alignment=ft.MainAxisAlignment.CENTER, expand=True),
                                ft.Container(
                                    content=ft.Icon(
                                        ft.Icons.ARROW_FORWARD_IOS,
                                        size=16,
                                        color=middle_color
                                    ),
                                    padding=10
                                )
                            ], spacing=15),
                            padding=20,
                            on_click=lambda e, item=item: maintenance_details_dialog(page, item)
                        ),
                        elevation=2,
                        margin=ft.margin.symmetric(vertical=5)
                    )
                    maintenance_cards.append(maintenance_card)
            else:
                maintenance_cards.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.BUILD_OUTLINED, size=60, color=ft.Colors.GREY_400),
                            ft.Text("No hay órdenes de mantenimiento registradas", size=16, color=ft.Colors.GREY_500)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                        padding=40,
                        alignment=ft.alignment.center
                    )
                )
            
            return [ft.Column(controls=maintenance_cards, spacing=10)]
        
        return []
    
    content_container = ft.Column(
        controls=create_content(),
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
        scroll=ft.ScrollMode.AUTO
    )
    
    def update_cards():
        nonlocal spare_data
        spare_data = get_all_spares()
        content_container.controls = create_content()
        content_container.update()
    
    return ft.Column(
        controls= [
           search_bar,
           ft.Divider(height= 20, color= ft.Colors.GREY_300),
           ft.Container(
               content=content_container,
               expand=True
           )
        ],
        horizontal_alignment= ft.CrossAxisAlignment.CENTER,
        alignment= ft.MainAxisAlignment.START,
        expand= True,
        spacing= 10
    )

def technician_spare_details(*, page: ft.Page, code: int, name: str, quantity: int, image_src: str = None):
    """Diálogo de detalles de pieza para técnicos (solo lectura + solicitar pieza)"""
    
    # Imagen de la pieza
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
    
    # Información de la pieza (solo lectura)
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
                    ft.Text(f"{quantity} unidades disponibles", size=16, color=dark_grey_color)
                ], spacing=8)
            ], spacing=12),
            padding=20,
            width=300
        ),
        elevation=2
    )
    
    # Campo para cantidad a solicitar (más bonito)
    quantity_field = ft.Container(
        content=ft.TextField(
            label="Cantidad a solicitar",
            keyboard_type=ft.KeyboardType.NUMBER,
            prefix_icon=ft.Icons.SHOPPING_CART,
            border_radius=15,
            border_color=middle_color,
            focused_border_color=purple_color,
            label_style=ft.TextStyle(color=middle_color),
            text_style=ft.TextStyle(size=16),
            content_padding=ft.padding.symmetric(horizontal=15, vertical=12)
        ),
        width=280,
        padding=ft.padding.all(5)
    )
    
    def request_spare(e):
        try:
            requested_qty = int(quantity_field.content.value or 0)
            if requested_qty <= 0:
                page.snack_bar = ft.SnackBar(content=ft.Text("Ingrese una cantidad válida"))
                page.snack_bar.open = True
                page.update()
                return
            
            if requested_qty > quantity:
                page.snack_bar = ft.SnackBar(content=ft.Text("Cantidad solicitada excede el stock disponible"))
                page.snack_bar.open = True
                page.update()
                return
            
            # Aquí iría la lógica para crear la solicitud de pieza
            page.close(dialog)
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Solicitud de {requested_qty} unidades de {name} enviada"))
            page.snack_bar.open = True
            page.update()
            
        except ValueError:
            page.snack_bar = ft.SnackBar(content=ft.Text("Ingrese un número válido"))
            page.snack_bar.open = True
            page.update()
    
    # Botones de acción para técnicos
    action_buttons = ft.Row([
        ft.ElevatedButton(
            text="Solicitar Pieza",
            icon=ft.Icons.SHOPPING_CART,
            bgcolor=middle_color,
            color=ft.Colors.WHITE,
            on_click=request_spare
        ),
        ft.OutlinedButton(
            text="Cerrar",
            on_click=lambda _: page.close(dialog)
        )
    ], spacing=10, alignment=ft.MainAxisAlignment.CENTER)
    
    dialog = ft.AlertDialog(
        title=ft.Row([
            ft.Icon(ft.Icons.SETTINGS, color=purple_color),
            ft.Text("Detalles de la Pieza", size=20, weight=ft.FontWeight.BOLD)
        ], spacing=10),
        content=ft.Column([
            container_img,
            ft.Divider(height=20),
            info_card,
            ft.Divider(height=10),
            quantity_field,
            ft.Divider(height=10),
            action_buttons
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
        content_padding=30
    )
    page.open(dialog)

def technician_equipment_details(page: ft.Page, equipment):
    """Diálogo de detalles de equipo para técnicos (solo lectura)"""
    
    # Icono del equipo
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
    
    # Información del equipo (solo lectura)
    info_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.TAG, color=purple_color, size=20),
                    ft.Text(f"#{equipment.code}", size=16, weight=ft.FontWeight.BOLD, color=purple_color)
                ], spacing=8),
                ft.Row([
                    ft.Icon(ft.Icons.INVENTORY, color=dark_grey_color, size=20),
                    ft.Text(equipment.name, size=16, weight=ft.FontWeight.BOLD)
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
    
    dialog = ft.AlertDialog(
        title=ft.Row([
            ft.Icon(ft.Icons.PRECISION_MANUFACTURING, color=purple_color),
            ft.Text("Información del Equipo", size=20, weight=ft.FontWeight.BOLD)
        ], spacing=10),
        content=ft.Column([
            equipment_icon,
            ft.Divider(height=20),
            info_card,
            ft.Divider(height=10),
            ft.Text(
                "Solo lectura - Contacta a tu supervisor para modificaciones",
                size=12,
                color=ft.Colors.GREY_500,
                italic=True,
                text_align=ft.TextAlign.CENTER
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
        actions=[
            ft.OutlinedButton(
                text="Cerrar",
                on_click=lambda _: page.close(dialog)
            )
        ],
        content_padding=30
    )
    page.open(dialog)