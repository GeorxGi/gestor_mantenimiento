import flet as ft

from src.views.welcome_page_view import WelcomePage

def main(page: ft.Page):
    page.title= 'Gestor mantenimiento'
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 500
    page.bgcolor = ft.Colors.GREY_100
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def route_change(e):
        match page.route:
            case '/':
                if not page.views:
                    page.views.append(WelcomePage(page).build())
            case '/login':
                from src.views.login.login_view import LoginView
                page.views.append(LoginView(page).build())
            case _:
                page.views.append(ft.View(
                    route='/404',
                    controls=[ft.Text('ERROR: Página no encontrada', size= 30)],
                    vertical_alignment= ft.MainAxisAlignment.CENTER
                ))
        page.update()

    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1] if page.views else None
        page.go(top_view.route if top_view else "/")
        page.update()

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.views.append(WelcomePage(page).build())
    page.go('/')

ft.app(
    target= main,
    view= ft.AppView.WEB_BROWSER,
    assets_dir="assets",
)