import flet as ft
from src.utils.routes import register_view

from src.views.supervisor.inventory_view import inventory
from src.views.supervisor.profile_view import profile_set


from src.consts.colors import purple_color,blue_color
from src.widgets.gradient_text import gradient_text
from src.consts.colors import gradient_colors

class ButtonsAdd(ft.ElevatedButton):
    def __init__(self, text, on_click_event):
        super().__init__()
        self.content = ft.Text(text, 
                               color=ft.Colors.WHITE,
                               size=15)
        self.on_click_event = on_click_event
        self.bgcolor = ft.Colors.BLUE
        self.color = ft.Colors.WHITE
        self.width = 250

class SupervisorView:
    def __init__(self, page: ft.Page):
        self.page = page
        
        self.add_options = ft.BottomSheet(
            ft.Container(
                ft.Column(
                    [
                        ft.Text("Añadir...", 
                                color=ft.Colors.GREY_500,
                                weight=ft.FontWeight.BOLD,
                                size=25),
                        ButtonsAdd("Equipo", on_click_event=lambda _: print("Evento de añadir equipo")),
                        ButtonsAdd("Orden de mantenimiento", on_click_event=lambda _: print("Evento de orden de mantenimiento")),
                        ButtonsAdd("Solicitud de pieza", on_click_event=lambda _: print("Evento de solicitud de pieza")),
                    ]
                ),
                alignment=ft.alignment.center,
                width=350,
                height=250,
                padding=10,
            )
        )
    
        self.content_area = ft.Column(
                controls=[],
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
        )
        self.content_area.controls.append(inventory(self.page))
    
    def on_navigation(self, e):
        selected_index = e.control.selected_index
        self.content_area.controls.clear()
        match selected_index:
            case 0:
                self.content_area.controls.append(inventory(self.page))
            case 1:
                self.page.open(self.add_options)
            case 2:
                self.content_area.controls.append(profile_set(self.page))
                
        self.content_area.update()
    
    def build(self):
        return ft.View(
            # este appbar puede ser global para todas las vistas de nivel de acceso
            appbar= ft.AppBar(
                automatically_imply_leading=False,
                leading= ft.IconButton(
                    icon= ft.Icons.DARK_MODE_OUTLINED  if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.Icons.DARK_MODE,
                ),
                bgcolor= ft.Colors.WHITE,
                title= gradient_text(
                    text= "HAC",
                    size= 30,
                    text_weight= ft.FontWeight.BOLD,
                    gradient= gradient_colors,
                ),
                center_title= True,
                actions= [
                    ft.IconButton(icon=ft.Icons.MESSAGE_OUTLINED,
                              tooltip= "Mensajes",
                              icon_color= ft.Colors.BLACK,
                            #   on_click= lambda _: self.page.go('/messages')
                    ),
                    
                ]
            ),
            bottom_appbar= ft.NavigationBar(
                selected_index= 0,
                on_change = self.on_navigation,
                height=100,
                bgcolor= ft.Colors.WHITE,
                destinations= [
                    ft.NavigationBarDestination(
                        icon=ft.Icons.HOME_OUTLINED,
                        label = "Inventario",
                        selected_icon= ft.Icons.HOME
                    ),
                    ft.NavigationBarDestination(
                        icon=ft.Icons.ADD,
                        label="Agregar"
                    ),
                    ft.NavigationBarDestination(
                        icon=ft.Icons.ACCOUNT_CIRCLE_OUTLINED,
                        label = "Perfil",
                        selected_icon= ft.Icons.ACCOUNT_CIRCLE
                    ),
                    
                ]
                ),
            route= '/supervisor',
            controls= [
                self.content_area
            ],
        )
        
if __name__ == '__main__':
    print('Cargando supervisor en modo debug')

    def test_supervisor_page(page: ft.Page):
        page.title= "Supervisor (DEBUG MODE)"
        page.window.resizable = True
        page.window.width = 500
        page.theme_mode = ft.ThemeMode.LIGHT
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.views.append(SupervisorView(page).build())
        page.go('/supervisor')

    ft.app(
        target=test_supervisor_page
    )