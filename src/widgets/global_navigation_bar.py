import flet as ft

from src.consts.colors import *
from src.enums.access_level import AccessLevel


def global_navigation_bar(page: ft.Page, access_level: AccessLevel, on_change_callback) -> ft.NavigationBar:
    # Cambiar label según el tipo de usuario
    first_label = "Órdenes" if access_level == AccessLevel.TECHNICIAN else "Inventario"
    first_icon = ft.Icons.ASSIGNMENT if access_level == AccessLevel.TECHNICIAN else ft.Icons.HOME_OUTLINED
    first_selected_icon = ft.Icons.ASSIGNMENT_TURNED_IN if access_level == AccessLevel.TECHNICIAN else ft.Icons.HOME
    
    destinations = [
        ft.NavigationBarDestination(
            icon=first_icon,
            label=first_label,
            selected_icon=first_selected_icon
        ),
        ft.NavigationBarDestination(
            icon=ft.Icons.ACCOUNT_CIRCLE_OUTLINED,
            label="Perfil",
            selected_icon=ft.Icons.ACCOUNT_CIRCLE
        ),
    ]
    
    # Solo supervisores pueden agregar
    if access_level == AccessLevel.SUPERVISOR:
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
    
    # Solo administradores pueden ver trabajadores
    if access_level == AccessLevel.ADMIN:
        destinations.insert(1, ft.NavigationBarDestination(
            icon=ft.Icons.PEOPLE_OUTLINE,
            label="Trabajadores",
            selected_icon=ft.Icons.PEOPLE
        ))
    
    return ft.NavigationBar(
        selected_index=0,
        on_change=on_change_callback,
        height=100,
        bgcolor=ft.Colors.WHITE,
        destinations=destinations
    )