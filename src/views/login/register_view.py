import flet as ft
from src.utils.routes import register_view

from src.widgets.gradient_text import gradient_text
from src.widgets.custom_text_field import CustomTextField
from src.widgets.gradient_button import gradient_button
from src.consts.colors import gradient_colors
from src.controllers.user.session_controller import register_user

@register_view("/register")
class RegisterView:
    def __init__(self, page: ft.Page):
        self.page = page
    
    def _register(self):
        email = self.email_text_field.value
        username = self.username_text_field.value
        password = self.password_text_field.value
        access_level = self.access_level_DropDown.value
        agreement = self.CheckBox_Agreement.value
        
        if not email or not username or not password or not access_level:
            self.page.open(
                self.local_snack_bar('Rellene los campos')
            )
            return
        if agreement == False:
            self.page.open(
                self.local_snack_bar('Debe aceptar los términos y condiciones')
            )
            return
        
    def local_snack_bar(error:str)-> ft.SnackBar:
        return ft.SnackBar(
        bgcolor= ft.Colors.BLUE,
        content= ft.Text(
            value= error,
            color= ft.Colors.WHITE
        ),
    )
        
    email_text_field = CustomTextField(
        hint_label= "Correo electrónico",
        width= 350,
        icon= ft.Icons.EMAIL
    )
    username_text_field = CustomTextField(
        hint_label= "Usuario",
        width= 350,
        icon= ft.Icons.ACCOUNT_CIRCLE_ROUNDED,
    )
    password_text_field = CustomTextField(
        hint_label= "Contraseña",
        width= 350,
        icon= ft.Icons.HTTPS,
        is_pass= True,
    )
    access_level_DropDown = ft.Dropdown(
        width= 350,
        hint_text= "Nivel de acceso",
        leading_icon=ft.Icon(ft.Icons.SUPERVISOR_ACCOUNT),
        options= [
            ft.dropdown.Option("Supervisor"),
            ft.dropdown.Option("Administrador"),
            ft.dropdown.Option("Usuario"),
        ],
        color= ft.Colors.GREY_500,
        border_color= ft.Colors.GREY_300,
        focused_border_color= ft.Colors.GREY_500,
        text_size= 14,
        text_style= ft.TextStyle(
            color= ft.Colors.GREY_500,
        ),
        border_radius= ft.border_radius.all(10),
        content_padding= ft.padding.only(left= 10, right= 10),
    )
    _main_view_container = ft.Container(
        height= 500,
        bgcolor= ft.Colors.WHITE,
        border_radius= ft.border_radius.all(20),
        border= ft.border.all(1, ft.Colors.GREY_200),
        content= ft.Column(
            alignment= ft.MainAxisAlignment.CENTER,
            horizontal_alignment= ft.CrossAxisAlignment.CENTER,
            spacing= 10,
            controls= [
                gradient_text(
                    text= "HAC",
                    size= 60,
                    text_weight= ft.FontWeight.BOLD,
                    gradient= gradient_colors,
                ),
                ft.Container(
                    alignment= ft.alignment.center,
                    margin= ft.margin.only(bottom= 10),
                    content= ft.Text(
                        value= "¡Bienvenido!",
                        size= 15,
                        color= ft.Colors.GREY_500,
                    ),
                ),
                email_text_field,
                username_text_field,
                password_text_field,
                access_level_DropDown,
            ],
        ),
    )
    
    CheckBox_Agreement =  ft.CupertinoCheckbox(
                        value= False,
                        active_color="#8855ff"
                    )
    
    Agreement = ft.Column(
        controls= [
            ft.Row(
                controls= [
                    CheckBox_Agreement,
                    ft.Text(
                        value= "",
                        spans=[
                            ft.TextSpan(
                                text= "Acepto los ",
                                style=ft.TextStyle(
                                    size=16,
                                    color=ft.Colors.GREY_500,
                                ),
                            ),
                            ft.TextSpan(
                                text= "términos y condiciones",
                                url= "https://www.macroplastics.com/images/docs/Terminos-y-Condiciones-de-Venta.pdf",
                                style=ft.TextStyle(
                                    size=16,
                                    color=ft.Colors.BLUE
                                ),
                            ),
                        ]
                    ),
                ],
            ),
        ],
    )
    
    def build(self) -> ft.View:
        """Inicializar la interfaz de Register"""
        return ft.View(
            appbar= ft.AppBar(),
            route= '/register',
            vertical_alignment= ft.MainAxisAlignment.CENTER,
            horizontal_alignment= ft.CrossAxisAlignment.CENTER,
            scroll= ft.ScrollMode.AUTO,
            controls= [
                ft.Text(
                    value= "REGISTRO DE USUARIO",
                    weight= ft.FontWeight.BOLD,
                    size= 30,
                    color= ft.Colors.GREY,
                ),
                self._main_view_container,
                ft.Container(
                    agreement := self.Agreement,
                ),
                gradient_button(
                    text= "Continuar",
                    width= 300,
                    height= 48,
                    gradient= gradient_colors,
                    on_click= lambda e: self._register(),
                ),
            ],
        )
    
if __name__ == '__main__':
    print('Cargando register en modo debug')

    def test_register_page(page: ft.Page):
        page.title= "Register (DEBUG MODE)"
        page.window.resizable = True
        page.window.width = 500
        page.theme_mode = ft.ThemeMode.LIGHT
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.views.append(RegisterView(page).build())
        page.go('/register')

    ft.app(
        target=test_register_page
    )

        
        
        
    
        
        