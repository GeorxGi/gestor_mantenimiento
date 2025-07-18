import flet as ft
from src.utils.routes import register_view

from src.widgets.gradient_button import gradient_button
from src.widgets.gradient_text import gradient_text
from src.consts.colors import gradient_colors, middle_color

@register_view('/')
class WelcomePage:
    def __init__(self, page: ft.Page):
        self.page = page

    def _go_to_login(self):
        self.page.go('/login')

    def _go_to_register(self):
        self.page.go('/register')

    def build(self) -> ft.View:
        """Iniciar la interfaz de bienvenida"""
        return ft.View(
            route= '/',
            controls= [
                ft.Column(
                    alignment= ft.MainAxisAlignment.CENTER,
                    horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                    expand= True,
                    spacing= 20,
                    controls= [
                        gradient_text(
                            text= 'HAC',
                            size= 80,
                            gradient= gradient_colors,
                        ),
                        
                        ft.Text(
                            "Bienvenido!",
                            size= 20,
                            color= ft.Colors.GREY_700
                        ),
                        gradient_button(
                            on_click= lambda e: self._go_to_login(),
                            text='Iniciar sesión',
                            gradient=gradient_colors,
                            width=350,
                            height= 48,
                        ),
                        ft.OutlinedButton(
                            content= gradient_text(text='Registrarse', gradient=gradient_colors, size=20),
                            on_click= lambda e: self._go_to_register(),
                            width= 300,
                            height= 48,
                            icon_color= ft.Colors.WHITE,
                            style= ft.ButtonStyle( side= ft.BorderSide(2, ft.Colors.GREY_300),) #Borde del boton
                        ),
                    ]
                )
            ],
            horizontal_alignment= ft.CrossAxisAlignment.CENTER,
            vertical_alignment= ft.MainAxisAlignment.CENTER,
            bgcolor= ft.Colors.GREY_100
        )


if __name__ == '__main__':
    print('Cargando pantalla de bienvenida en modo DEBUG')
    #ft.app(target= lambda page: WelcomePage(page).build())

    def test_welcome_page(page: ft.Page):
        page.title= "Welcome page (DEBUG MODE)"
        page.window.resizable = True
        page.theme_mode = ft.ThemeMode.LIGHT
        page.window.width = 500
        page.bgcolor = ft.Colors.GREY_100
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.views.append(WelcomePage(page).build())
        page.go('/')

    ft.app(
        target= test_welcome_page
    )