import flet as ft

from src.consts.colors import *

def global_navigation_bar(page: ft.Page, access_level: str, on_change_callback) -> ft.NavigationBar:
    destinations = [
        ft.NavigationBarDestination(
            icon=ft.Icons.HOME_OUTLINED,
            label="Inventario",
            selected_icon=ft.Icons.HOME
        ),
        ft.NavigationBarDestination(
            icon=ft.Icons.ACCOUNT_CIRCLE_OUTLINED,
            label="Perfil",
            selected_icon=ft.Icons.ACCOUNT_CIRCLE
        ),
    ]
    
    # Solo supervisores pueden agregar
    if access_level == "SUPERVISOR":
        destinations.insert(1, ft.NavigationBarDestination(
            icon=ft.Container(
                content=ft.Icon(ft.Icons.ADD, color=ft.Colors.WHITE, size=20),
                bgcolor=middle_color,
                border_radius=20,
                width=60,
                height=35,
                alignment=ft.alignment.center
            ),
            selected_icon=ft.Container(
                content=ft.Icon(ft.Icons.ADD, color=ft.Colors.WHITE, size=20),
                bgcolor=middle_color,
                border_radius=20,
                width=60,
                height=35,
                alignment=ft.alignment.center
            ),
            label="Agregar"
        ))
    
    return ft.NavigationBar(
        selected_index=0,
        on_change=on_change_callback,
        height=100,
        bgcolor=ft.Colors.WHITE,
        destinations=destinations
    )