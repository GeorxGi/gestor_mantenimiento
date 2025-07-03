import flet as ft

def spare_details_window(page: ft.Page, code, name, quantity=0, image_src=None):
    
    container_img = ft.Container(
        width=100,
        height=100,
        bgcolor=ft.Colors.GREY_200,
        border_radius=15,
        alignment=ft.alignment.center,
        content=ft.Image(src=image_src, fit=ft.ImageFit.COVER, border_radius=ft.border_radius.all(13)) if image_src else ft.Icon(
            ft.Icons.IMAGE,
            size=50,
            color=ft.Colors.GREY_300
        )
    )
    
    dialog = ft.AlertDialog(
        title=ft.Text("Detalles de la pieza", size=18, weight=ft.FontWeight.BOLD),
        content=ft.Column([
            container_img,
            ft.Divider(height=20),
            ft.Text(f"Código: #{code}", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
            ft.Text(f"Nombre: {name}", size=14),
            ft.Text(f"Cantidad: {quantity}", size=14)
        ], tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
        actions=[
            ft.TextButton("Cerrar", on_click=lambda e: page.close(dialog))
        ]
    )
    page.open(dialog)