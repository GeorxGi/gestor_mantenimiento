import flet as ft

def equipment_details_dialog(page: ft.Page, code, name, status="Activo", location="No especificada", model="No especificado"):
    
    dialog = ft.AlertDialog(
        title=ft.Text("Detalles del equipo", size=18, weight=ft.FontWeight.BOLD),
        content=ft.Column([
            ft.Text(f"Código: #{code}", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700),
            ft.Text(f"Nombre: {name}", size=14),
            ft.Text(f"Estado: {status}", size=14),
            ft.Text(f"Ubicación: {location}", size=14),
            ft.Text(f"Modelo: {model}", size=14)
        ], tight=True, horizontal_alignment=ft.CrossAxisAlignment.START, spacing=8),
        actions=[
            ft.TextButton("Cerrar", on_click=lambda e: page.close(dialog))
        ]
    )
    page.open(dialog)