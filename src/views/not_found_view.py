import flet as ft
from src.utils.routes import register_view

@register_view('/404')
class NotFound:
    def __init__(self, page: ft.Page):
        self.page = page

    def _go_to_start(self):
        self.page.go('/')

    def build(self):
        return ft.View(
            appbar= ft.AppBar(),
            route= '/404',
            vertical_alignment= ft.MainAxisAlignment.CENTER,
            horizontal_alignment= ft.CrossAxisAlignment.CENTER,
            spacing= 30,
            controls=[
                ft.Text(
                    value= 'ERROR\nPágina no encontrada',
                    size= 30,
                    text_align= ft.TextAlign.CENTER
                ),
            ]
        )