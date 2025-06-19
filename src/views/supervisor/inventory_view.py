import flet as ft 

def inventory(page: ft.Page):
    return ft.Column(
        [
            ft.Text("Aqui va el inventario", size=50)
        ],
        horizontal_alignment= ft.CrossAxisAlignment.CENTER,
        alignment= ft.MainAxisAlignment.START,
        expand= True,
        spacing= 0
        )