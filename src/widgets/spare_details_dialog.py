import flet as ft

from src.enums.access_level import AccessLevel

from src.consts.colors import *

from src.models.spare import Spare

from src.utils.notification_handler import notify_admins

from src.controllers.spare_controller import remove_spare_from_inventory, discount_spare_stock, add_spare_stock
from src.widgets.custom_snack_bar import custom_snack_bar

from src.widgets.dialog_button import dialog_button
from src.widgets.input_form import input_form

def spare_details_window(*, page: ft.Page, spare:Spare, user_access_level:AccessLevel):

    def ammount_dialog(action:str, title:str):

        def act():
            if action == "request":
                notify_admins(event= "Pieza solicitada", content= f"Se ha solicitado reposición de la pieza {spare.name} - #{spare.code}")
                page.open(custom_snack_bar(content= "Solicitud de pieza enviada"))

            elif action == "discount":
                discount_spare_stock(spare_code=spare.code, request_ammount= int(ammount_input.value))
                page.open(custom_snack_bar(content="Piezas descontadas de inventario"))

            elif action == "replace":
                add_spare_stock(spare_code= spare.code, to_add_amount= int(ammount_input.value))
                page.open(custom_snack_bar(content="Piezas repuestas correctamente"))

            page.close(local_dialog)


        ammount_input = input_form(
            input_filter= ft.InputFilter(
                regex_string=r"^[0-9]*$"
            ),
            icon= ft.Icons.NUMBERS,
            label= "Cantidad"
        )
        local_dialog= ft.AlertDialog(
        title= title,
        content=ammount_input,
        actions_alignment= ft.alignment.center,
        actions= [
            ft.ElevatedButton(
                text= "Aceptar",
                icon= ft.Icons.CHECK,
                on_click= lambda _: act()
            ),
            ft.ElevatedButton(
                text= "Cancelar",
                icon= ft.Icons.CANCEL,
                on_click= lambda _: page.close(local_dialog)
            )
        ]
    )
        return local_dialog

    def confirm_delete():

        def remove_spare(spare_code:int):
            if remove_spare_from_inventory(spare_code):
                page.open(custom_snack_bar(content="Pieza eliminada exitosamente"))
                page.close(alert_dialog)
            else:
                page.open(custom_snack_bar(content="La pieza no pudo ser encontrada o no pudo ser eliminada"))
                page.close(alert_dialog)

        alert_dialog= ft.AlertDialog(
            content= ft.Text("Está seguro de que desea eliminar esta pieza?\nESTA ACCION NO SE PUEDE DESHACER"),
            actions= [
                ft.Button(
                   "Eliminar",
                    color= ft.Colors.RED_300,
                    icon= ft.Icons.DELETE,
                    on_click= lambda _: remove_spare(spare.code)
                ),
                ft.ElevatedButton(
                    content= ft.Text("Cancelar"),
                    color= blue_color,
                    icon= ft.Icons.CANCEL,
                    text= "Cancelar",
                    on_click= lambda _: page.close(alert_dialog)
                )
            ]
        )
        page.open(alert_dialog)

    def request_quantity():
        user_data = page.session.get('local_user')
        if not user_data.get('assigned_maintenance_id', ""):
            page.open(custom_snack_bar(content="No posee mantenimiento seleccionado, operación rechazada"))
        else:
            page.open(
                ammount_dialog(
                    title= f"Ingrese la cantidad de {spare.name} a solicitar de inventario",
                    action="discount"
                )
            )
    
    def request_spare():
        page.open(
            ammount_dialog(
                title= f"Solicitar reposición para {spare.name}",
                action= "request"
            )
        )
    
    def replace():
        user_data = page.session.get('local_user')
        if user_data.get("access_level", "") != AccessLevel.ADMIN.name:
            page.open(custom_snack_bar(content="No es ADMIN, no puede reponer"))
            return
        page.open(ammount_dialog(
                title= f"Cantidad de {spare.name} a reponer",
                action= 'replace'
            )
        )
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
            text="Eliminar",
            icon=ft.Icons.DELETE,
            bgcolor=ft.Colors.RED_300,
            on_click=lambda _: confirm_delete()
        )
    ]

    if user_access_level == AccessLevel.TECHNICIAN and spare.amount > 0:
        buttons_list.insert(0, dialog_button(
            text="Solicitar pieza para mantenimiento",
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
            src=spare.image_path,
            fit=ft.ImageFit.COVER,
            border_radius=ft.border_radius.all(13)) if spare.image_path else ft.Icon(
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
                ft.Text(value= f"Código: #{spare.code}", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
                ft.Text(value= f"Nombre: {spare.name}", size=14),
                ft.Text(value= f"Cantidad: {spare.amount}", size=14),
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