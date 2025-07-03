import flet as ft

from src.enums.access_level import AccessLevel
from src.enums.register_cases import RegisterCases

from src.widgets.gradient_text import gradient_text
from src.widgets.custom_text_field import CustomTextField
from src.widgets.gradient_button import gradient_button
from src.widgets.custom_snack_bar import custom_snack_bar
from src.utils.routes import register_view

from src.consts.colors import gradient_colors
from src.controllers.user.session_controller import register_user

@register_view('/register')
class RegisterView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.fullname_text_field = CustomTextField(
            hint_label= 'Nombre completo',
            width= 350,
            icon= ft.Icons.PERSON,
            on_submit= lambda _: self.email_text_field.focus()
        )
        self.email_text_field = CustomTextField(
            hint_label= "Correo electrónico",
            width= 350,
            icon= ft.Icons.EMAIL,
            on_submit= lambda _: self.username_text_field.focus()
        )
        self.username_text_field = CustomTextField(
            hint_label= "Usuario",
            width= 350,
            icon= ft.Icons.ACCOUNT_CIRCLE_ROUNDED,
            on_submit= lambda _: self.password_text_field.focus()
        )
        self.password_text_field = CustomTextField(
            hint_label= "Contraseña",
            width= 350,
            icon= ft.Icons.HTTPS,
            is_pass= True,
            on_submit= lambda _: self.access_level_DropDown.focus()
        )
        self.access_level_DropDown = ft.Dropdown(
            width= 350,
            hint_text= "Nivel de acceso",
            leading_icon=ft.Icon(ft.Icons.SUPERVISOR_ACCOUNT),
            options= [
                ft.dropdown.Option(text= "Administrador", key= str(AccessLevel.ADMIN.value)),
                ft.dropdown.Option(text="Supervisor", key= str(AccessLevel.SUPERVISOR.value)),
                ft.dropdown.Option(text= "Técnico", key= str(AccessLevel.TECHNICIAN.value)),
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
        self.main_view_container = ft.Container(
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
                    self.fullname_text_field,
                    self.email_text_field,
                    self.username_text_field,
                    self.password_text_field,
                    self.access_level_DropDown,
                ],
            ),
        )

        self.CheckBox_Agreement =  ft.CupertinoCheckbox(
        value= False,
        active_color="#8855ff",
        )

        self.Agreement = ft.Row(
            vertical_alignment= ft.CrossAxisAlignment.CENTER,
            alignment= ft.MainAxisAlignment.CENTER,
            controls= [
                self.CheckBox_Agreement,
                ft.Text(
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
        )

    def _close_view(self):
        self._reset_fields()
        self.page.views.pop()
        self.page.update()

    def _reset_fields(self):
        self.username_text_field.value = ''
        self.password_text_field.value = ''
        self.email_text_field.value = ''
        self.access_level_DropDown.value = None
    
    def _register(self):
        email = self.email_text_field.value
        fullname = self.fullname_text_field.value
        username = self.username_text_field.value
        password = self.password_text_field.value
        agreement = self.CheckBox_Agreement.value

        #este pequeño bloque es para parsear
        if self.access_level_DropDown.value is not None:
            access_level = AccessLevel(int(self.access_level_DropDown.value))
        else:
            access_level = None

        if not agreement:
            self.page.open(custom_snack_bar(content= 'Debe aceptar los términos y condiciones'))
            return

        register_result = register_user(
            username=username,
            password=password,
            email= email,
            access_level= access_level,
            fullname= fullname
        )
        if register_result == RegisterCases.CORRECT:
            self.page.open(custom_snack_bar(content= 'Registro realizado exitosamente'))
            self._close_view()
            return
        else:
            self.page.open(custom_snack_bar(content= str(register_result.value)))
    
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
                self.main_view_container,
                self.Agreement,
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
        page.window.height = 900
        page.theme_mode = ft.ThemeMode.LIGHT
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.views.append(RegisterView(page).build())
        page.go('/register')

    ft.app(
        target=test_register_page
    )