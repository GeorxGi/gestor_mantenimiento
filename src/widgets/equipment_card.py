import flet as ft
from src.consts.colors import *

def equipment_card(code="1234", name="Equipo", status="Activo", on_click=None) -> ft.GestureDetector:
    
    container_img = ft.Container(
        width=120,
        height=70,
        bgcolor=ft.Colors.GREEN_50,
        border_radius=15,
        alignment=ft.alignment.center,
        border=ft.border.all(2, ft.Colors.GREEN_200),
        content=ft.Icon(
            ft.Icons.PRECISION_MANUFACTURING,
            size=35,
            color=ft.Colors.GREEN_600
        )
    )
    
    code_text = ft.Text(
        f"#{code}", 
        size=11, 
        color=ft.Colors.GREEN_700,
        weight=ft.FontWeight.BOLD
    )
    
    name_text = ft.Text(
        name, 
        size=12, 
        color=ft.Colors.GREY_800,
        weight=ft.FontWeight.W_500,
        text_align=ft.TextAlign.CENTER,
        max_lines=2,
        overflow=ft.TextOverflow.ELLIPSIS
    )
    
    status_text = ft.Text(
        status,
        size=10,
        color=ft.Colors.GREEN_600,
        weight=ft.FontWeight.BOLD
    )
    
    container_card = ft.Container(
        width=200,
        height=150,
        bgcolor=ft.Colors.WHITE,
        border_radius=16,
        padding=15,
        alignment=ft.alignment.center,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=8,
            color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            offset=ft.Offset(0, 2)
        ),
        border=ft.border.all(1, ft.Colors.GREY_100),
        content=ft.Column(
            controls=[
                container_img,
                ft.Container(height=8),
                code_text,
                name_text,
                status_text
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4
        )
    )
    
    return ft.GestureDetector(
        content=container_card,
        on_tap=on_click,
        mouse_cursor=ft.MouseCursor.CLICK
    )