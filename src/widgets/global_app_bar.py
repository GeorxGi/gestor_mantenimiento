import flet as ft

from src.widgets.gradient_text import gradient_text
from src.consts.colors import gradient_colors



def global_app_bar(page: ft.Page, access_level: str) -> ft.AppBar:
    print(f"DEBUG AppBar - Access level recibido: '{access_level}'")
    
    actions = []
    if access_level == "SUPERVISOR":
        print("DEBUG AppBar - Agregando botón de mensajes para supervisor")
        actions = [
            ft.IconButton(
                icon=ft.Icons.MESSAGE_OUTLINED,
                tooltip="Mensajes",
                icon_color=ft.Colors.BLACK,
                # on_click=lambda _: page.go('/messages')
            )
        ]
    else:
        print(f"DEBUG AppBar - No es supervisor, es: '{access_level}'")
    
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