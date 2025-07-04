import flet as ft

from src.consts.colors import *
from src.enums.access_level import AccessLevel


def global_navigation_bar(page: ft.Page, access_level: AccessLevel, on_change_callback) -> ft.NavigationBar:
    destinations = [
        ft.NavigationBarDestination(
            icon=ft.Icons.HOME_OUTLINED,
            label="Inventario",
            selected_icon=ft.Icons.HOME
        )
    ]
    
    # indince supervisor
    if access_level == AccessLevel.SUPERVISOR:
        destinations.append(ft.NavigationBarDestination(
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
    
    # indice solo admin
    if access_level == AccessLevel.ADMIN:
        destinations.append(ft.NavigationBarDestination(
            icon=ft.Icons.PEOPLE_ALT_OUTLINED,
            label="Trabajadores",
            selected_icon=ft.Icons.PEOPLE
        ))
    
    #se agrega como ultimo indice siempre
    destinations.append(ft.NavigationBarDestination(
        icon=ft.Icons.ACCOUNT_CIRCLE_OUTLINED,
        label="Perfil",
        selected_icon=ft.Icons.ACCOUNT_CIRCLE
    ))
    
    return ft.NavigationBar(
        selected_index=0,
        on_change=on_change_callback,
        height=100,
        bgcolor=ft.Colors.WHITE,
        destinations=destinations
    )