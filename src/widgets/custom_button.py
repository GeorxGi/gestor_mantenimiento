import flet as ft


def custom_button(text: str, width: int, height:int, gradient: list[ft.Colors], icon: str, on_click) -> ft.Container:
    
    contentainer_icon = ft.Container(
        width= 0.40 * width,
        height= 0.40 * width,
        padding= ft.padding.all(20),
        border_radius=ft.border_radius.all(100),
        bgcolor= ft.Colors.WHITE,
        content=ft.Icon(
            name= icon,
            size= 0.15 * width,
            color= ft.Colors.WHITE
        ),
        alignment= ft.alignment.center,
        gradient= ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=gradient,
        ),
    )
    
    content = ft.Column(
        controls=[
            contentainer_icon,
            ft.Text(
                value= text,
                size= 0.10 * width,
                color= ft.Colors.GREY_700,
                weight= ft.FontWeight.BOLD
            )
        ],
        horizontal_alignment= ft.CrossAxisAlignment.CENTER,
        alignment= ft.MainAxisAlignment.CENTER,
        spacing= 10
    )
    
    
    return ft.Container(
        width= width,
        height=height,
        border_radius=ft.border_radius.all(20),
        border=ft.border.all(1, ft.Colors.GREY_300),
        bgcolor= ft.Colors.WHITE,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=ft.Colors.with_opacity(0.1, ft.Colors.BLUE_GREY_900),
            offset=ft.Offset(0, 0),
        ),
        content=ft.ElevatedButton(
            content=content,
            expand=True,
            width=width,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.TRANSPARENT,
                overlay_color=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                shadow_color=ft.Colors.TRANSPARENT,
                surface_tint_color=ft.Colors.TRANSPARENT,
            ),
            on_click=on_click
        )
    )