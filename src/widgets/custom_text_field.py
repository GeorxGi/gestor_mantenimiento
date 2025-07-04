import flet as ft

def CustomTextField(*, hint_label:str, width:int, is_pass:bool = False, icon:ft.Icons, on_submit = None) -> ft.TextField:
    return ft.TextField(
        on_submit= on_submit,
        label= hint_label,
        border_color= ft.Colors.BLUE,
        width= width,
        border=ft.InputBorder.UNDERLINE,
        border_radius=ft.border_radius.all(10),
        can_reveal_password= is_pass,
        icon= icon,
        password= is_pass,
        text_style= ft.TextStyle(
            size=20,
            color=ft.Colors.GREY_700
        )
    )