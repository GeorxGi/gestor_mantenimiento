# movi el inventario de lugar ya que los 3 niveles de acceso pueden visualizar el inventario

import flet as ft
from src.enums.access_level import AccessLevel

from src.consts.colors import middle_color

from src.widgets.spare_card import spare_card
from src.widgets.spare_details_dialog import spare_details_window
from src.widgets.equipment_details_dialog import equipment_details_dialog
from src.widgets.filter_dialog import filter_dialog

from src.controllers.equipment_controller import get_equipment_by_partial_name
from src.controllers.spare_controller import get_spare_by_partial_name

from src.controllers.maintenance_controller import get_all_maintenances

def inventory(page: ft.Page):
    
    # quiero hacer una opcion para que se pueda interactuar con el view de inventario dependiendo del nivel de acceso
    
    # 1er paso: obtengo el nivel de acceso
    user_data = page.session.get("local_user")
    user_access_level: AccessLevel = AccessLevel.from_string(user_data.get("access_level")) if user_data else AccessLevel.USER
    
    # aqui agregué como opcion el boton de filtrar, los mantenimientos pendientes (solo lo pueden ver los admin y sup)
    show_pieces = ft.Ref[bool]()
    show_equipment = ft.Ref[bool]()
    show_maintenance = ft.Ref[bool]() 
    show_pieces.current = True
    show_equipment.current = False
    show_maintenance.current = False

    # Piezas de la base de datos
    spare_objects = get_spare_by_partial_name('')
    # Equipos de la base de datos
    equipment_objects = []
    maintenance_objects = []

    def add_filters():
        if show_pieces.current:
            nonlocal spare_objects
            spare_objects = get_spare_by_partial_name(search_field.value)
        elif show_equipment.current:
            nonlocal equipment_objects
            equipment_objects = get_equipment_by_partial_name(search_field.value)

        update_cards()

    search_field = ft.TextField(
        hint_text="buscar por nombre...",
        prefix_icon=ft.Icons.SEARCH,
        width=300,
        on_submit= lambda _: add_filters(),
        border_radius= ft.border_radius.all(30),
        border_color=ft.Colors.GREY_300)


    # luis: aqui no se si prefieras georges agregar una busqueda a las ordenes de mantenimiento ya sea por nombre de tecnicos, fecha, o xyz
    def update_filters(pieces, equipment, maintenance):
        show_pieces.current = pieces
        show_equipment.current = equipment
        show_maintenance.current = maintenance
        if show_pieces.current:
            nonlocal spare_objects
            spare_objects = get_spare_by_partial_name('')
        elif show_equipment.current:
            nonlocal equipment_objects
            equipment_objects = get_equipment_by_partial_name('')
        elif show_maintenance.current:
            nonlocal maintenance_objects
            maintenance_objects = get_all_maintenances()
        
        update_cards()
    
    def open_filter_dialog(e):
        filter_dialog(page, update_filters)
    
    search_bar = ft.Row(
        controls= [
            search_field,
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
    
    def create_content():
        if show_pieces.current:
            # Crear filas de 2 cards para piezas
            cards = [
                spare_card(
                    image_src= spare.image_path,
                    code=spare.code,
                    name=spare.name,
                    on_click=lambda _, code = spare.code, name = spare.name, quantity = spare.amount, img_pth = spare.image_path:
                    spare_details_window(page= page,code= code,name=  name, quantity= quantity, image_src= img_pth, user_access_level=user_access_level)
                ) for spare in spare_objects
            ]
            
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
            if equipment_objects:
                equipment_list = [
                    ft.ListTile(
                        leading= ft.Icon(ft.Icons.PRECISION_MANUFACTURING, color= ft.Colors.GREEN_600),
                        title= ft.Text(value= f"#{equipment.code}", weight= ft.FontWeight.BOLD),
                        subtitle= ft.Text(equipment.name),
                        on_click= lambda _, item= equipment: equipment_details_dialog(
                            page, item
                        )
                    ) for equipment in equipment_objects
                ]
            else:
                equipment_list.append(
                    ft.Text(value= "No hay equipos registrados", color=ft.Colors.GREY_500, size=16)
                )

            return [ft.Column(controls= equipment_list, spacing= 5)]
        
        elif show_maintenance.current:
            # Crear lista simple para mantenimientos
            maintenance_list = []
            if maintenance_objects:
                maintenance_list = [
                    ft.ListTile(
                        leading= ft.Icon(ft.Icons.BUILD, color= ft.Colors.ORANGE_600),
                        title= ft.Text(value= f"#{maintenance.id}", weight= ft.FontWeight.BOLD),
                        subtitle= ft.Text(f"Equipo: {maintenance.equipment_code} - {maintenance.details[:50]}..."),
                        trailing= ft.Icon(
                            ft.Icons.PENDING if maintenance.is_pending else ft.Icons.CHECK_CIRCLE,
                            color= ft.Colors.ORANGE if maintenance.is_pending else ft.Colors.GREEN
                        )
                    ) for maintenance in maintenance_objects
                ]
            else:
                maintenance_list.append(
                    ft.Text(value= "No hay mantenimientos registrados", color=ft.Colors.GREY_500, size=16)
                )

            return [ft.Column(controls= maintenance_list, spacing= 5)]
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