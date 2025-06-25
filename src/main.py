import flet as ft
from controllers.sql.base_sql import BaseSqlController

def main(page: ft.Page):
    BaseSqlController.init_db()
    page.title= 'Gestor mantenimiento'
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 500
    page.window.height = 900
    page.bgcolor = ft.Colors.GREY_100
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def route_change(e):
        print(f"Moviendo la ruta a: {page.route}")

        #Evita que se intente duplicar una página
        if page.views and page.views[-1].route == page.route:
            return

        from src.utils.routes import get_view
        from src.views.not_found_view import NotFound

        # Obtiene vista del registro o 404
        view = get_view(page, page.route) or NotFound(page).build()
        page.views.append(view)
        page.update()

    def view_pop(e):
        if len(page.views) > 1:
            page.views.pop()
            page.go(page.views[-1].route)
            page.update()

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go('/')

ft.app(
    target= main,
    view= ft.AppView.FLET_APP,
    assets_dir="assets",
)