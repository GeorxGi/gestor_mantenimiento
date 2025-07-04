import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import flet as ft

from src.controllers.sql.base_sql import BaseSqlController
from src.utils.notification_handler import listening_sessions

def main(page: ft.Page):
    BaseSqlController.init_db()
    page.title= 'Gestor mantenimiento'
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 500
    page.window.height = 900
    page.bgcolor = ft.Colors.GREY_100
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.on_disconnect = lambda _: listening_sessions.pop(page.session_id, None)
    page.scroll = ft.ScrollMode.AUTO
    print("* new_session: ", page.session_id)

    def route_change(_):
        #Evita que se intente duplicar una página
        if page.views and page.views[-1].route == page.route:
            return

        from src.utils.routes import get_view
        from src.views.not_found_view import NotFound

        # Obtiene vista del registro o 404
        view = get_view(page, page.route) or NotFound(page).build()
        page.views.append(view)
        page.update()

    def view_pop(_):
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
    upload_dir='assets/uploads'
)