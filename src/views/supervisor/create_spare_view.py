import flet as ft   

from src.widgets.gradient_button import gradient_button
from src.widgets.input_form import input_form

from src.consts.colors import gradient_colors, middle_color

def create_spare_view(page:ft.Page, on_success=None):
    code_input = input_form(label="Codigo", icon=ft.Icons.QR_CODE_2)
    quantity_input = input_form(label="Cantidad", icon=ft.Icons.NUMBERS)

    title_form = ft.Column(
        controls = [
            ft.Icon(
                ft.Icons.EXTENSION,
                size= 80,
                color= middle_color
                ),
            ft.Text(
                value="Agregar solicitud de pieza",
                size= 25,
                weight= ft.FontWeight.BOLD,
                color= ft.Colors.GREY_700
            ),
            ft.Divider(height= 15, color= ft.Colors.GREY_300),
        ],
        alignment= ft.MainAxisAlignment.CENTER,
        horizontal_alignment= ft.CrossAxisAlignment.CENTER,
        spacing= 10
    )
    
    container_img_piece = ft.Container(
        width= 150,
        height= 150,
        bgcolor= ft.Colors.GREY_300,
        border_radius= 20,
        content= ft.Icon(
            ft.Icons.IMAGE,
            size= 100,
            color= ft.Colors.WHITE
        )
    )
    
    container_form = ft.Container(
        width= 400,
        height= 500,
        bgcolor=ft.Colors.WHITE,
        border= ft.border.all(1, ft.Colors.GREY_300),
        border_radius= 20,
        padding= ft.padding.all(20),
        content = ft.Column(
            alignment= ft.MainAxisAlignment.CENTER,
            horizontal_alignment= ft.CrossAxisAlignment.CENTER,
            controls=[
                title_form,
                container_img_piece,
                code_input,
                quantity_input,
            ]
        )
    )
    
    return ft.Container(
        content = ft.Column(
            controls=[
                container_form,
                gradient_button(
                    text= 'agregar',
                    width=300,
                    height=48,
                    gradient= gradient_colors,
                    on_click= lambda e: print('guarda pieza'),
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        ),
        alignment=ft.alignment.center,
        expand=True
    )
    