###
### Diseñar GUI para el inicio se sesión
###

import flet as ft
from flet_gradient_text import GradientText

container = ft.Container(content=ft.Column(
        [
           GradientText("HAC", 
                   text_size=80,
                   text_weight=ft.FontWeight.BOLD,
                   gradient=ft.LinearGradient(
                        begin=ft.alignment.top_left,
                        end=ft.alignment.bottom_right,
                        colors=["#8855ff", ft.Colors.BLUE_400], # Colores del gradiente para el texto
                    ),
                   ),
           ft.Container(
               content=ft.Text("Bienvenido usuario, ingrese los siguientes datos", 
                               size=15, 
                               color=ft.Colors.GREY_500),
               alignment=ft.alignment.center,
               margin=ft.margin.only(bottom=20)
           ),
            ft.TextField(label="Usuario", 
                        border_color=ft.Colors.BLUE,
                        width=350,
                        border=ft.InputBorder.UNDERLINE,
                        border_radius=ft.border_radius.all(10),
                        icon=ft.Icons.ACCOUNT_CIRCLE_ROUNDED,
                        text_style= ft.TextStyle(
                            size=20,
                            color=ft.Colors.GREY_700
                        )
                        ),
            
            ft.TextField(label="Contraseña",
                         border_color=ft.Colors.BLUE,
                         width=350,
                         border=ft.InputBorder.UNDERLINE,
                         border_radius=ft.border_radius.all(10),
                         can_reveal_password=True,
                         icon=ft.Icons.HTTPS,
                         password=True,
                         text_style= ft.TextStyle(
                            size=20,
                            color=ft.Colors.GREY_700
                        )),
            ft.TextButton(text="Olvidé mi contraseña",
                         icon_color=ft.Colors.BLUE,
                        )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
    height=500,
    bgcolor=ft.Colors.WHITE,
    border_radius=ft.border_radius.all(20),
    border=ft.border.all(1, ft.Colors.GREY_200)
)

def main(page: ft.Page):
    page.title = "Flet container"
    page.window.resizable = True
    page.window.width = 500
    page.bgcolor = ft.Colors.GREY_100
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    titulo_empresa = ft.Text("INICIO DE SESION", 
                             weight=ft.FontWeight.BOLD,
                             size=30, color=ft.Colors.GREY)
    
    login_btn_content = ft.Text(
        "Iniciar Sesión",
        size=20,
        color=ft.Colors.WHITE,
    )

    actual_button = ft.ElevatedButton(
        content=login_btn_content,
        width=300,

        style=ft.ButtonStyle(
            bgcolor=ft.Colors.TRANSPARENT, 
            overlay_color=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
            shadow_color=ft.Colors.TRANSPARENT,
            surface_tint_color=ft.Colors.TRANSPARENT, 
        ),
        on_click=lambda e: print("aqui evento de click para redireccion..."),
    )

    gradient_button_container = ft.Container(
        content=actual_button, 
        width=300, 
        height=48, 
        gradient=ft.LinearGradient(
            begin=ft.alignment.center_left,
            end=ft.alignment.center_right,
            colors=["#8855ff", ft.Colors.BLUE_400], 
        ),
        border_radius=ft.border_radius.all(22),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=ft.Colors.with_opacity(0.3, ft.Colors.BLUE_GREY_900),
            offset=ft.Offset(0, 0),
        ),
        margin=ft.margin.only(top=20), 
    )
    
    page.add(ft.Column(
            [
                titulo_empresa,
                container,
                gradient_button_container
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        ))
    
ft.app(target=main)
###
