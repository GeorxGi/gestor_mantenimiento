import flet as ft

def profile_set(page: ft.Page):
    return ft.Column(
        [
            ft.Text("Aqui va el perfil", size=50)
        ],
        horizontal_alignment= ft.CrossAxisAlignment.CENTER,
        alignment= ft.MainAxisAlignment.START,
        expand= True,
        spacing= 0
    )