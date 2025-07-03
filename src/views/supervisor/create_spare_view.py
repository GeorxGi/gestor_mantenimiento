import base64

import flet as ft

from src.widgets.custom_snack_bar import custom_snack_bar
from src.widgets.gradient_button import gradient_button
from src.widgets.input_form import input_form

from src.consts.colors import gradient_colors, middle_color

from src.controllers.spare_controller import add_spare
from src.enums.create_spare_cases import CreateSpareCases

def create_spare_view(page:ft.Page, on_success=None):
    picked_image_bytes = None

    def register_spare():
        quantity  = 0
        if quantity_input.value.isnumeric():
            quantity = int(quantity_input.value)
        result = add_spare(
            name= name_input.value,
            amount= quantity,
            image_bytes= picked_image_bytes
        )
        page.open(custom_snack_bar(content= result.value))
        if result == CreateSpareCases.CORRECT:
            if on_success:
                on_success()

    def pick_image(_):
        file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["png", "jpg", "jpeg", "bmp"],
        )

    def on_file_picked(e: ft.FilePickerResultEvent):
        nonlocal picked_image_bytes

        if e.files:
            selected_file = e.files[0]
            picked_image_bytes = getattr(selected_file, "bytes", None)

            # Si no hay bytes, intenta leer desde el path
            if picked_image_bytes is None and hasattr(selected_file, "path") and selected_file.path:
                try:
                    with open(selected_file.path, "rb") as f:
                        picked_image_bytes = f.read()
                except Exception as ex:
                    page.open(custom_snack_bar(content=f"Error al leer la imagen: {ex}"))
                    page.update()
                    return

            if picked_image_bytes:
                image_preview.content = ft.Image(
                    src_base64=base64.b64encode(picked_image_bytes).decode("utf-8"),
                    width=150,
                    height=150,
                    fit=ft.ImageFit.COVER
                )
            else:
                page.open(custom_snack_bar(content="Ocurrió un error a la hora de cargar la imágen"))
            page.update()
    
    file_picker = ft.FilePicker(on_result=on_file_picked)
    page.overlay.append(file_picker)

    picked_file: None | bytes = None
    
    code_input = input_form(label="Código de pieza", icon=ft.Icons.QR_CODE_2)
    code_input.disabled = True
    
    name_input = input_form(
        label="Nombre",
        icon=ft.Icons.EDIT_ROUNDED)
    quantity_input = input_form(
        label="Cantidad",
        icon=ft.Icons.NUMBERS,
        keyboard_type= ft.KeyboardType.NUMBER,
        input_filter= ft.InputFilter(
            allow= True,
            regex_string= r"^[0-9]*$"
        )
    )

    title_form = ft.Column(
        controls = [
            ft.Icon(
                ft.Icons.EXTENSION,
                size= 80,
                color= middle_color
                ),
            ft.Text(
                value="Agregar pieza",
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
    
    image_preview = ft.Container(
        width= 150,
        height= 150,
        bgcolor= ft.Colors.GREY_300,
        border_radius= 20,
        alignment= ft.alignment.center,
        content= ft.Icon(
            ft.Icons.IMAGE,
            size= 100,
            color= ft.Colors.WHITE
            )
        )
    
    row_image = ft.Stack(
        controls=[
            ft.Container(
            height=150,
                content=image_preview,
                alignment=ft.alignment.center
            ),
            ft.Container(
                content=ft.IconButton(
                    icon= ft.Icons.PUBLISH,
                    icon_color= ft.Colors.WHITE,
                    bgcolor= ft.Colors.GREY_700,
                    icon_size= 20,
                    on_click= pick_image,
                ),
                alignment=ft.alignment.bottom_right,
                margin=ft.margin.only(right=10, bottom=10)
            )
        ],
    )
    
    container_form = ft.Container(
        width= 400,
        height= 550,
        bgcolor=ft.Colors.WHITE,
        border= ft.border.all(1, ft.Colors.GREY_300),
        border_radius= 20,
        padding= ft.padding.all(20),
        content = ft.Column(
            alignment= ft.MainAxisAlignment.CENTER,
            horizontal_alignment= ft.CrossAxisAlignment.CENTER,
            controls=[
                title_form,
                row_image,
                code_input,
                quantity_input,
                name_input,
            ]
        )
    )
    
    return ft.Container(
        content = ft.Column(
            scroll= ft.ScrollMode.AUTO,
            controls=[
                container_form,
                gradient_button(
                    text= 'agregar',
                    width=300,
                    height=48,
                    gradient= gradient_colors,
                    on_click= lambda _: register_spare()
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        ),
        alignment=ft.alignment.center,
        expand=True
    )
    