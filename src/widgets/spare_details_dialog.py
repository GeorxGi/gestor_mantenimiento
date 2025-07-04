import flet as ft

def spare_details_window(*, page: ft.Page, code:int, name:str, quantity:int, image_src:str = None):
    
    container_img = ft.Container(
        width=100,
        height=100,
        bgcolor=ft.Colors.GREY_200,
        border_radius=15,
        alignment=ft.alignment.center,
        content=ft.Image(
            src=image_src,
            fit=ft.ImageFit.COVER,
            border_radius=ft.border_radius.all(13)) if image_src else ft.Icon(
            ft.Icons.IMAGE,
            size=50,
            color=ft.Colors.GREY_300
        )
    )
    
    dialog = ft.AlertDialog(
        title=ft.Text(value= "Detalles de la pieza", size=18, weight=ft.FontWeight.BOLD),
        content=ft.Column(controls= [
            container_img,
            ft.Divider(height=20),
            ft.Text(value= f"Código: #{code}", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
            ft.Text(value= f"Nombre: {name}", size=14),
            ft.Text(value= f"Cantidad: {quantity}", size=14)
        ], tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
        actions=[
            ft.TextButton(text= "Cerrar", on_click=lambda _: page.close(dialog))
        ]
    )
    page.open(dialog)