import flet as ft

from src.enums.access_level import AccessLevel

from src.consts.colors import *
from src.widgets.dialog_button import dialog_button



def spare_details_window(*, page: ft.Page, code:int, name:str, quantity:int, image_src:str = None, user_access_level:AccessLevel):
    
    def request_quantity():
        print('funcion para solicitud de reposicion')
    
    def request_spare():
        print('funcion para solicitud de pieza')
    
    def replace():
        print('funcion para reposicion de pieza')
        
    buttons_list = [
        dialog_button(
            text="Cerrar",
            icon=ft.Icons.CLOSE,
            bgcolor=ft.Colors.RED_300,
            on_click=lambda _: page.close(dialog)
        )
    ]
    
    buttons_high_level = [
        dialog_button(
            text="Editar",
            icon=ft.Icons.EDIT,
            bgcolor=ft.Colors.GREEN_300,
            on_click=lambda _: print('editar')
        ),
        dialog_button(
            text="Eliminar",
            icon=ft.Icons.DELETE,
            bgcolor=ft.Colors.RED_300,
            on_click=lambda _: print('eliminar')
        )
    ]

    if user_access_level == AccessLevel.TECHNICIAN and quantity > 0:
        buttons_list.insert(0, dialog_button(
            text="Solicitar cantidad",
            icon=ft.Icons.REQUEST_QUOTE,
            bgcolor=middle_color,
            on_click=lambda _: request_quantity()
        ))
    elif user_access_level == AccessLevel.SUPERVISOR:
        buttons_list.extend(buttons_high_level)
        buttons_list.insert(0, dialog_button(
            text="Solicitar reposición",
            icon=ft.Icons.REQUEST_QUOTE,
            bgcolor=middle_color,
            on_click=lambda _: request_spare()
        ))
    elif user_access_level == AccessLevel.ADMIN:
        buttons_list.extend(buttons_high_level)
        buttons_list.insert(0, dialog_button(
            text="Reponer pieza",
            icon=ft.Icons.ADD,
            bgcolor=middle_color,
            on_click=lambda _: replace()
        ))
        
    container_img = ft.Container(
        width=100,
        height=100,
        bgcolor=ft.Colors.GREY_200,
        border_radius=15,
        alignment=ft.alignment.center,
        content=ft.Image(
            src=image_src,
            fit=ft.ImageFit.COVER,
            border_radius=ft.border_radius.all(13)) if image_src else ft.Icon(
            ft.Icons.IMAGE,
            size=50,
            color=ft.Colors.GREY_300
        )
    )
    
    # Separar botón cerrar de los demás
    action_buttons = [btn for btn in buttons_list if "Cerrar" not in btn.text]
    close_button = dialog_button(
        text="Cerrar",
        icon=ft.Icons.CLOSE,
        bgcolor=ft.Colors.RED_300,
        on_click=lambda _: page.close(dialog)
    )
    
    dialog = ft.AlertDialog(
        title=ft.Text(value= "Detalles de la pieza", size=18, weight=ft.FontWeight.BOLD),
        content=ft.Column(
            width=400,
            controls= [
                container_img,
                ft.Divider(height=20),
                ft.Text(value= f"Código: #{code}", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
                ft.Text(value= f"Nombre: {name}", size=14),
                ft.Text(value= f"Cantidad: {quantity}", size=14),
                ft.Divider(height=10),
                # Fila de botones de acción
                ft.Row(
                    controls=action_buttons,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10
                ) if action_buttons else ft.Container(),
                # Botón cerrar en esquina derecha
                ft.Row(
                    controls=[close_button],
                    alignment=ft.MainAxisAlignment.END
                )
            ], tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8)
    )
    page.open(dialog)