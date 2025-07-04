import flet as ft 
from src.consts.colors import *
from src.widgets.spare_card import spare_card
from src.widgets.spare_details_dialog import spare_details_window
from src.widgets.equipment_details_dialog import equipment_details_dialog
from src.widgets.filter_dialog import filter_dialog
from src.controllers.equipment_controller import get_all_equipments
from src.controllers.maintenance_controller import get_all_maintenance_orders, get_supervisor_pending_maintenances, conclude_maintenance
from src.controllers.spare_controller import get_all_spares
from src.consts.file_dir import SPARE_IMAGES_PATH
import os

def inventory(page: ft.Page):
    
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
            "provider": eq.provider  # Usando provider como modelo temporalmente
        }
        for eq in equipment_objects
    ]
    
    # Obtener órdenes de mantenimiento de la base de datos
    maintenance_objects = get_all_maintenance_orders()
    maintenance_data = [
        {
            "id": maint.id,
            "equipment_code": maint.equipment_code,
            "details": maint.details,
            "date": str(maint.maintenance_date),
            "status": "Pendiente" if maint.is_pending else "Completado"
        }
        for maint in maintenance_objects
    ]
    
    # Obtener mantenimientos pendientes del supervisor
    user_data = page.session.get("local_user")
    supervisor_id = user_data.get("id", "") if user_data else ""
    pending_maintenance_objects = get_supervisor_pending_maintenances(supervisor_id)
    pending_maintenance_data = [
        {
            "id": maint.id,
            "equipment_code": maint.equipment_code,
            "details": maint.details,
            "date": str(maint.maintenance_date)
        }
        for maint in pending_maintenance_objects
    ]
    
    def create_content():
        if show_pieces.current:
            # Crear filas de 2 cards para piezas
            cards = []
            for item in spare_data:
                # Verificar si existe imagen para esta pieza
                image_path = os.path.join(SPARE_IMAGES_PATH, f"{item['code']}.jpg")
                image_src = str(image_path) if os.path.exists(image_path) else None
                
                card = spare_card(
                    code=item["code"],
                    name=item["name"],
                    image_src=image_src,
                    on_click=lambda e, c=item["code"], n=item["name"], q=item["quantity"]: spare_details_window(page, c, n, q)
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
            # Crear lista simple para equipos
            equipment_list = []
            if equipment_data:
                for item in equipment_data:
                    equipment_item = ft.ListTile(
                        style= ft.border_radius.all(20),
                        leading=ft.Icon(ft.Icons.PRECISION_MANUFACTURING, color=purple_color),
                        title=ft.Text(item["name"], weight=ft.FontWeight.BOLD, color=dark_grey_color),
                        subtitle=ft.Text(f"#{item['code']}", color=grey_color),
                        # quiero poner un trailing de editar y eliminar
                        on_click=lambda e, item=item: equipment_details_dialog(
                            page, item["code"], item["name"], item["description"], item["provider"]
                        )
                    ) for equipment in equipment_objects
                ]
            else:
                equipment_list.append(
                    ft.Text(value= "No hay equipos registrados", color=ft.Colors.GREY_500, size=16)
                )
            
            return [ft.Column(controls=equipment_list, spacing=5)]
        
        elif show_maintenance.current:
            # Crear lista para órdenes de mantenimiento
            maintenance_list = []
            if maintenance_data:
                for item in maintenance_data:
                    status_color = ft.Colors.ORANGE if item["status"] == "Pendiente" else ft.Colors.GREEN
                    maintenance_item = ft.ListTile(
                        leading=ft.Icon(ft.Icons.BUILD, color=status_color),
                        title=ft.Text(f"Equipo: {item['equipment_code']}", weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text(f"{item['details']} - {item['date']}"),
                        trailing=ft.Chip(
                            label=ft.Text(item["status"]),
                            bgcolor=status_color,
                            label_style=ft.TextStyle(color=ft.Colors.WHITE)
                        )
                    )
                    maintenance_list.append(maintenance_item)
            else:
                maintenance_list.append(
                    ft.Text("No hay órdenes de mantenimiento registradas", color=ft.Colors.GREY_500, size=16)
                )
            
            return [ft.Column(controls=maintenance_list, spacing=5)]
        

        
        return []
    
    content_container = ft.Column(
        controls=create_content(),
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
        scroll=ft.ScrollMode.AUTO
    )
    
    def update_cards():
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