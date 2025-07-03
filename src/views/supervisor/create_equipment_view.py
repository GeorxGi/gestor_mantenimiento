import flet as ft

from src.enums.create_equipment_cases import CreateEquipmentCases

from src.widgets.custom_snack_bar import custom_snack_bar
from src.widgets.gradient_button import gradient_button
from src.widgets.input_form import input_form

from src.consts.colors import gradient_colors, middle_color

from src.controllers.equipment_controller import create_equipment

def create_equipment_view(page: ft.Page, on_success = None):
    code_input = input_form(label="Codigo", icon=ft.Icons.QR_CODE_2)
    name_input = input_form(label="Nombre", icon=ft.Icons.CREATE)
    description_input = input_form(label="Descripcion", icon=ft.Icons.ASSIGNMENT)
    provider_input = input_form(label="Proveedor", icon=ft.Icons.STORE)

    def register_equipment():
        response = create_equipment(
            name= name_input.value,
            description= description_input.value,
            provider= provider_input.value,
            code= code_input.value
        )
        if response == CreateEquipmentCases.CORRECT:
            page.open(custom_snack_bar(content=str(response.value)))
            if on_success:
                on_success()
        else:
            page.open(custom_snack_bar(content= str(response.value)))

    title_form = ft.Column(
        controls= [
            # main_img,
            ft.Icon(
                ft.Icons.PRECISION_MANUFACTURING,
                size= 80,
                color= middle_color
            ),
            ft.Text(
                value="Agregar equipo",
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
                code_input,
                name_input,
                description_input,
                provider_input,
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
                    on_click= lambda e: register_equipment()
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        ),
        alignment=ft.alignment.center,
        expand=True
    )

