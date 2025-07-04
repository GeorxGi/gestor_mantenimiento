import flet as ft

from src.consts.colors import *

def dialog_button(text: str, icon:str, bgcolor:str, on_click) -> ft.ElevatedButton:
    return ft.ElevatedButton(
        text=text,
        icon=icon,
        bgcolor=bgcolor if not text == "Cerrar" else ft.Colors.WHITE,
        color= ft.Colors.RED_300 if text == "Cerrar" else ft.Colors.WHITE,
        on_click=on_click
    )