import flet as ft
from src.consts.colors import *

def equipment_details_dialog(page: ft.Page, code, name, description, provider="No especificado"):
    
    dialog = ft.AlertDialog(
        title=ft.Row([
            ft.Icon(ft.Icons.PRECISION_MANUFACTURING, color=purple_color, size=28),
            ft.Text("Detalles del Equipo", size=20, weight=ft.FontWeight.BOLD, color=dark_grey_color)
        ], spacing=10),
        content=ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.TAG, color=white_color, size=20),
                        ft.Text(f"{code}", size=18, weight=ft.FontWeight.BOLD, color=white_color)
                    ], spacing=8),
                    padding=ft.padding.all(10),
                    bgcolor=purple_color,
                    border_radius=8
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.LABEL, color=dark_grey_color, size=18),
                            ft.Text("Nombre:", weight=ft.FontWeight.BOLD, color=dark_grey_color)
                        ], spacing=5),
                        ft.Text(name, size=16, color=ft.Colors.BLACK87)
                    ], spacing=5),
                    padding=10
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.DESCRIPTION, color=dark_grey_color, size=18),
                            ft.Text("Descripción:", weight=ft.FontWeight.BOLD, color=dark_grey_color)
                        ], spacing=5),
                        ft.Text(description, size=16, color=ft.Colors.BLACK87)
                    ], spacing=5),
                    padding=10
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.BUSINESS, color=dark_grey_color, size=18),
                            ft.Text("Proveedor:", weight=ft.FontWeight.BOLD, color=dark_grey_color)
                        ], spacing=5),
                        ft.Text(provider, size=16, color=ft.Colors.BLACK87)
                    ], spacing=5),
                    padding=10
                )
            ], spacing=15),
            width=400,
            height=300,
            padding=10
        ),
        actions=[
            ft.ElevatedButton(
                "Cerrar",
                icon=ft.Icons.CLOSE,
                bgcolor=ft.Colors.RED_400,
                color=ft.Colors.WHITE,
                on_click=lambda e: page.close(dialog)
            )
        ]
    )
    page.open(dialog)