import flet as ft

from src.consts.colors import *

def dialog_button(text: str, icon:str, bgcolor:str, on_click) -> ft.ElevatedButton:
    return ft.ElevatedButton(
        text=text,
        icon=icon,
        bgcolor=bgcolor,
        color=ft.Colors.WHITE,
        on_click=on_click
    )