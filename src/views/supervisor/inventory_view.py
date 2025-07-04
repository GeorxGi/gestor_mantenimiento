import flet as ft

from src.consts.colors import middle_color

from src.widgets.spare_card import spare_card
from src.widgets.spare_details_dialog import spare_details_window
from src.widgets.equipment_details_dialog import equipment_details_dialog
from src.widgets.filter_dialog import filter_dialog

from src.controllers.equipment_controller import get_equipment_by_partial_name
from src.controllers.spare_controller import get_spare_by_partial_name

def inventory(page: ft.Page):
    
    show_pieces = ft.Ref[bool]()
    show_equipment = ft.Ref[bool]()
    show_pieces.current = True
    show_equipment.current = False
    
    def update_filters(pieces, equipment):
        show_pieces.current = pieces
        show_equipment.current = equipment
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
    
    # Datos de ejemplo
    spare_data = get_spare_by_partial_name("")
    
    # Obtener equipos de la base de datos
    equipment_objects = get_equipment_by_partial_name("")
    equipment_data = [
        {
            "code": eq.code,
            "name": eq.name,
            "Descripción": eq.description,  # Agregar si tienes este campo
            "Proveedor": eq.provider  # Usando provider como modelo temporalmente
        }
        for eq in equipment_objects
    ]
    
    def create_content():
        if show_pieces.current:
            # Crear filas de 2 cards para piezas
            cards = [
                spare_card(
                    image_src= spare.image_path,
                    code=spare.code,
                    name=spare.name,
                    on_click=lambda _, code = spare.code, name = spare.name, quantity = spare.amount, img_pth = spare.image_path:
                    spare_details_window(page= page,code= code,name=  name, quantity= quantity, image_src= img_pth)
                ) for spare in spare_data
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