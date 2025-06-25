import flet as ft

from src.widgets.gradient_button import gradient_button
from src.widgets.input_form import input_form

from src.consts.colors import gradient_colors, middle_color
            
def equipment_form(page: ft.Page):
    title_form = ft.Column(
        controls= [
            # main_img,
            ft.Icon(
                ft.Icons.PRECISION_MANUFACTURING,
                size= 80,
                color= middle_color
            ),
            ft.Text("Agregar equipo",
                    size= 25,
                    weight= ft.FontWeight.BOLD,
                    color= ft.Colors.GREY_700
                    ),
            ft.Divider(height= 15, color= ft.Colors.GREY_300),
        ],
        alignment= ft.MainAxisAlignment.CENTER,
        horizontal_alignment= ft.CrossAxisAlignment.CENTER,
        spacing=5
    )
    container_form = ft.Container(
        width= 400,
        height= 500,
        bgcolor= ft.Colors.WHITE,
        border= ft.border.all(1, ft.Colors.GREY_300),
        border_radius= 20,
        padding= ft.padding.all(20),
        content= ft.Column(
            alignment= ft.MainAxisAlignment.CENTER,
            horizontal_alignment= ft.CrossAxisAlignment.CENTER,
            controls= [
                title_form,
                input_form(label="Codigo", icon=ft.Icons.QR_CODE_2),
                input_form(label="Nombre", icon=ft.Icons.CREATE),
                input_form(label="Descripcion", icon=ft.Icons.ASSIGNMENT),
                input_form(label="Proveedor", icon=ft.Icons.STORE)
            ],
        )
    )
    
    return ft.Container(
        content= ft.Column(
            controls=[
                container_form,
                gradient_button(
                    text= 'agregar',
                    width=300,
                    height=48,
                    gradient= gradient_colors,
                    on_click= lambda e: print('guarda equipo'),
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        ),
        alignment=ft.alignment.center,
        expand=True
    )

