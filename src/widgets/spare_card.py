import flet as ft

from src.consts.colors import middle_color

def spare_card(*, code:int | str, name:str, image_src:str = None, on_click=None) -> ft.GestureDetector:
    
    container_img = ft.Container(
        width=120,
        height=70,
        bgcolor=ft.Colors.GREY_100,
        border_radius=15,
        alignment=ft.alignment.center,
        content=
        ft.Image(
            src=image_src,
            fit=ft.ImageFit.COVER,
            border_radius=ft.border_radius.all(13)
        ) if image_src else ft.Icon(
            ft.Icons.IMAGE,
            size=35,
            color= ft.Colors.GREY_300
        )
    )
    
    code_spare = ft.Text(
        value= f"#{code}",
        size=11, 
        color= middle_color,
        weight=ft.FontWeight.BOLD
    )
    
    name_spare = ft.Text(
        name, 
        size=12, 
        color=ft.Colors.GREY_800,
        weight=ft.FontWeight.W_500,
        text_align=ft.TextAlign.CENTER,
        max_lines=2,
        overflow=ft.TextOverflow.ELLIPSIS
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
                code_spare,
                name_spare
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