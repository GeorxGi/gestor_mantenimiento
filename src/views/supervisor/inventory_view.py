import flet as ft 
from src.consts.colors import middle_color


def inventory(page: ft.Page):
    
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
                on_click= lambda e: print("despliega ventana emergente o menu para filtrar...")
            ),
        ],
        alignment= ft.MainAxisAlignment.CENTER,
        vertical_alignment= ft.CrossAxisAlignment.CENTER,
        spacing= 10
    )
    return ft.Column(
        [
           search_bar,
           ft.Divider(height= 20, color= ft.Colors.GREY_300)
        ],
        horizontal_alignment= ft.CrossAxisAlignment.CENTER,
        alignment= ft.MainAxisAlignment.START,
        expand= True,
        spacing= 0
        )