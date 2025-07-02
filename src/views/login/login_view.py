import flet as ft

from src.utils.routes import register_view

from src.widgets.gradient_text import gradient_text
from src.widgets.custom_text_field import CustomTextField
from src.widgets.gradient_button import gradient_button
from src.widgets.custom_snack_bar import custom_snack_bar

from src.consts.colors import gradient_colors
from src.controllers.user.session_controller import login_user

def _forgot_password():
    print('Evento para contraseña olvidada')
    pass
@register_view('/login')
class LoginView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.username_text_field = CustomTextField(
            hint_label= "Usuario",
            width= 350,
            icon= ft.Icons.ACCOUNT_CIRCLE_ROUNDED,
        )
        self.password_text_field = CustomTextField(
            hint_label= "Contraseña",
            width= 350,
            icon= ft.Icons.HTTPS,
            is_pass= True,
        )
        self.main_view_container = ft.Container(
            height=400,
            bgcolor=ft.Colors.WHITE,
            border_radius=ft.border_radius.all(20),
            border=ft.border.all(1, ft.Colors.GREY_200),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing= 10,
                controls= [
                    gradient_text(
                        text="HAC",
                        size=80,
                        text_weight= ft.FontWeight.BOLD,
                        gradient=gradient_colors,
                    ),
                    ft.Container(
                        alignment=ft.alignment.center,
                        margin=ft.margin.only(bottom=20),
                        content=ft.Text(
                            value= "¡Bienvenido!",
                            size=15,
                            color=ft.Colors.GREY_500),
                    ),
                    self.username_text_field,
                    self.password_text_field,
                    ft.TextButton(
                        text="Olvidé mi contraseña",
                        icon_color=ft.Colors.BLUE,
                        on_click= lambda e: _forgot_password()
                    ),
                ],
            ),
        )

    def _login(self):
        username = self.username_text_field.value
        password = self.password_text_field.value
        if not username or not password:
            self.page.open(custom_snack_bar(content= 'Rellene los campos'))
            return
        user = login_user(username= username, password= password)
        if not user:
            self.page.open(custom_snack_bar(content= 'Usuario o contraseña incorrectos'))
            return
        else:
            self.page.session.set(key= "local_user",value=  user.to_dict())
            self.page.session.set("welcome_shown", False)  # Reset welcome flag
            self.page.go('dashboard')

    def build(self) -> ft.View:
        """Inicializar la interfaz de login"""
        return ft.View(
            appbar= ft.AppBar(),
            route= '/login',
            vertical_alignment= ft.MainAxisAlignment.CENTER,
            horizontal_alignment= ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    value= "INICIO DE SESION",
                    weight=ft.FontWeight.BOLD,
                    size=30,
                    color=ft.Colors.GREY
                ),
                self.main_view_container,
                gradient_button(
                    text= 'Iniciar sesión',
                    width=300,
                    height=48,
                    gradient= gradient_colors,
                    on_click= lambda e: self._login(),
                ),
            ]
        )

if __name__ == '__main__':
    print('Cargando login en modo debug')

    def test_login_page(page: ft.Page):
        page.title= "Login (DEBUG MODE)"
        page.window.resizable = True
        page.window.width = 500
        page.theme_mode = ft.ThemeMode.LIGHT
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.views.append(LoginView(page).build())
        page.go('/login')

    ft.app(
        target=test_login_page
    )