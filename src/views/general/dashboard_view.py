import flet as ft

from src.enums.access_level import AccessLevel
from src.utils.routes import register_view
from src.utils.notification_handler import listen_to

from src.views.supervisor.create_equipment_view import create_equipment_view
from src.views.supervisor.create_maintenance_view import create_maintenance_view
from src.views.supervisor.create_spare_view import create_spare_view

from src.widgets.global_app_bar import global_app_bar
from src.widgets.global_navigation_bar import global_navigation_bar
from src.widgets.custom_snack_bar import custom_snack_bar

from src.views.supervisor.inventory_view import inventory
from src.views.general.profile_view import profile_set

from src.consts.colors import middle_color

class ButtonsAdd(ft.ElevatedButton):
    def __init__(self, text, on_click_event):
        super().__init__()
        self.content = ft.Text(text, 
                               color=ft.Colors.WHITE,
                               size=15)
        self.on_click = on_click_event
        self.bgcolor = middle_color
        self.color = ft.Colors.WHITE
        self.width = 250
        self.height = 40

@register_view('dashboard')
class DashboardView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.scroll = True
        
        # Obtener el nivel de acceso del usuario logueado
        user_data = self.page.session.get("local_user")

        self.access_level:AccessLevel = AccessLevel.from_string(user_data.get("access_level")) if user_data else AccessLevel.USER
        
        # Mostrar mensaje de bienvenida si viene del login
        if user_data and not self.page.session.get("welcome_shown"):
            listen_to(
                page= self.page,
                user_id= user_data.get("id", ""),
                access_level= AccessLevel.from_string(user_data.get("access_level", ""))
            )
            full_name = user_data.get("fullname", "Usuario")
            self.page.open(custom_snack_bar(content= f"¡Inicio de sesión exitoso! Bienvenido: {full_name}"))
            self.page.session.set(key= "welcome_shown",value= True)
        
        self.last_selected_index = 0

        def close_control_view():
            self.last_selected_index = 0
            self.close_add_options()

        def navigate_to(view_factory):
            self.page.close(self.add_options)
            self.content_area.controls.clear()
            self.content_area.controls.append(view_factory(self.page, on_success= close_control_view))
            self.content_area.update()
            self.page.update()

        self.add_options = ft.BottomSheet(
            ft.Container(
                ft.Column(
                    controls= [
                        ft.Text(
                            value="Agregar...",
                            color=ft.Colors.GREY_500,
                            weight=ft.FontWeight.BOLD,
                            size=25),
                        ButtonsAdd(text= "Equipo", on_click_event= lambda _: navigate_to(create_equipment_view)),
                        ButtonsAdd(text= "Orden de mantenimiento", on_click_event= lambda _: navigate_to(create_maintenance_view)),
                        ButtonsAdd(text= "Solicitud de pieza", on_click_event= lambda _: navigate_to(create_spare_view)),
                    ], 
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                    spacing=10
                ),
                alignment=ft.alignment.center,
                width=350,
                height=250,
                padding=20,
            ),
            # esto evita que al tocar afuera del bottonsheet se cierra
            dismissible=True,
            is_scroll_controlled=True,
            enable_drag=False
        )
    
        self.content_area = ft.Column(
            controls=[],
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )
        self.content_area.controls.append(inventory(self.page))
        
        # RETORNA EL INDICE SELECCIONADO
        self.navigation_bar = global_navigation_bar(self.page, self.access_level, self.on_navigation)
    
    def close_add_options(self):
        self.page.close(self.add_options)
        self.navigation_bar.selected_index = self.last_selected_index
        
        profile_index = 2 if self.access_level == AccessLevel.SUPERVISOR else 1
        
        self.content_area.controls.clear()
        if self.last_selected_index == 0:
            self.content_area.controls.append(inventory(self.page))
        elif self.last_selected_index == profile_index:
            self.content_area.controls.append(profile_set(self.page))
        
        self.content_area.update()
        self.page.update()
    
    def on_navigation(self, e):
        selected_index = e.control.selected_index

        add_index = 1 if self.access_level == AccessLevel.SUPERVISOR else None
        profile_index = 2 if self.access_level == AccessLevel.SUPERVISOR else 1

        if selected_index == add_index and self.access_level == AccessLevel.SUPERVISOR:
            self.page.open(self.add_options)

            e.control.selected_index = self.last_selected_index
            self.page.update()
            return

        self.last_selected_index = selected_index
        self.content_area.controls.clear()

        if selected_index == 0:
            self.content_area.controls.append(inventory(self.page))
        elif selected_index == profile_index:
            self.content_area.controls.append(profile_set(self.page))

        self.content_area.update()
    
    def build(self):
        # segun para que no salga el teclado
        self.page.window.prevent_close = False
        
        return ft.View(
            route= 'dashboard',
            appbar= global_app_bar(self.page, self.access_level),
            navigation_bar= self.navigation_bar,
            controls= [ self.content_area ],
        )
        
if __name__ == '__main__':
    print('Cargando dashborad en modo debug')

    def test_supervisor_page(page: ft.Page):
        page.title= "dashboard (DEBUG MODE)"
        page.window.resizable = True
        page.window.width = 500
        page.window.height =900
        page.theme_mode = ft.ThemeMode.LIGHT
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.views.append(DashboardView(page).build())
        page.go('/dashboard')

    ft.app(
        target=test_supervisor_page
    )