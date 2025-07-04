import flet as ft

from src.enums.access_level import AccessLevel
from src.widgets.gradient_text import gradient_text
from src.consts.colors import gradient_colors



def global_app_bar(page: ft.Page, access_level:AccessLevel) -> ft.AppBar:

    actions = []
    if access_level == AccessLevel.SUPERVISOR:
        actions = [
            ft.IconButton(
                icon=ft.Icons.MESSAGE_OUTLINED,
                tooltip="Mensajes",
                icon_color=ft.Colors.BLACK,
                # on_click=lambda _: page.go('/messages')
            )
        ]
    else:
        print(f"DEBUG AppBar - No es supervisor, es: '{access_level.value}'")
    
    return ft.AppBar(
        automatically_imply_leading=False,
        leading=ft.IconButton(
            icon=ft.Icons.DARK_MODE_OUTLINED if page.theme_mode == ft.ThemeMode.LIGHT else ft.Icons.DARK_MODE
        ),
        bgcolor=ft.Colors.WHITE,
        title=gradient_text(
            text="HAC",
            size=30,
            text_weight=ft.FontWeight.BOLD,
            gradient=gradient_colors,
        ),
        center_title=True,
        actions=actions
    )