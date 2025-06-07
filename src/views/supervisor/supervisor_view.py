import flet as ft

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
        
    add_options = ft.BottomSheet(
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
            height=300,
            padding=10,
        )
    )
    def on_navigation(self, e):
        selected_index = e.control.selected_index
        match selected_index:
            case 0:
                pass
            case 1:
                self.page.open(self.add_options)
                pass
            case 2:
                pass
                
        self.page.update()
    
    def build(self):
        return ft.View(
            bottom_appbar= ft.NavigationBar(
                selected_index= 0,
                on_change = self.on_navigation,
                destinations= [
                    ft.NavigationBarDestination(
                        icon=ft.Icons.STORAGE,
                        label = "Inventario",
                        selected_icon= ft.Icons.STORAGE_OUTLINED
                    ),
                    ft.NavigationBarDestination(
                        icon=ft.Icons.ADD,
                        label="Agregar"
                    ),
                    ft.NavigationBarDestination(
                        icon=ft.Icons.ACCOUNT_CIRCLE,
                        label = "Perfil",
                        selected_icon= ft.Icons.ACCOUNT_CIRCLE_OUTLINED
                    ),
                    
                ]
                ),
            route= '/supervisor',
            controls= [
                ft.Text(
                    value= "Vista de Supervisor",
                    weight= ft.FontWeight.BOLD, 
                    size= 30,
                    color= ft.Colors.GREY,
                ),
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