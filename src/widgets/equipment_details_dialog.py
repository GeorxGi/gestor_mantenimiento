import flet as ft
from src.consts.colors import *

from src.models.equipment import Equipment


def equipment_details_dialog(page: ft.Page, equipment:Equipment):
    
    dialog = ft.AlertDialog(
        title=ft.Text(value= "Detalles del equipo", size=18, weight=ft.FontWeight.BOLD),
        content=ft.Column(
            controls= [
                ft.Text(value= f"Código: #{equipment.code}", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700),
                ft.Text(value= f"Nombre: {equipment.name}", size=14),
                ft.Text(value= f"Detalles: {equipment.description}", size=14),
                ft.Text(value= f"Proveedor: {equipment.provider}", size=14),
        ], tight=True, horizontal_alignment=ft.CrossAxisAlignment.START, spacing=8),
        actions=[
            ft.TextButton(text= "Cerrar", on_click=lambda e: page.close(dialog))
        ]
    )
    page.open(dialog)