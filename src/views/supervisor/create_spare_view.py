import flet as ft   

from src.widgets.gradient_button import gradient_button
from src.widgets.input_form import input_form

from src.consts.colors import gradient_colors, middle_color

def create_spare_view(page:ft.Page, on_success=None):
    
    def pick_image(e):
        file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["png", "jpg", "jpeg", "gif", "bmp"]
        )
    
    def on_file_picked(e: ft.FilePickerResultEvent):
        if e.files:
            selected_file = e.files[0]
            container_img_piece.content = ft.Image(
                src=selected_file.path,
                width=150,
                height=150,
                fit=ft.ImageFit.COVER
            )
            page.update()
    
    file_picker = ft.FilePicker(on_result=on_file_picked)
    page.overlay.append(file_picker)
    
    code_input = input_form(label="numero ai de bd", icon=ft.Icons.QR_CODE_2)
    code_input.disabled = True
    
    name_input = input_form(label="Nombre", icon=ft.Icons.EDIT_ROUNDED)
    # Luis: no se si necesitas la cantidad para registrar la pieza, o de por si la cantidad = 0 de manera predeterminada
    quantity_input = input_form(label="Cantidad", icon=ft.Icons.NUMBERS)
    quantity_input.visible = False

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
    
    container_img_piece = ft.Container(
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
                content=container_img_piece,
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
                name_input,
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
    