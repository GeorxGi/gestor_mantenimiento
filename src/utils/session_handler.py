import flet as ft
from src.utils.notification_handler import listening_sessions

def logout(page: ft.Page):
    page.session.clear()
    listening_sessions.pop(page.session_id) if page.session_id is not None else None
    for value in listening_sessions:
        print(value)
    page.go('/')
    page.clean()
    page.update()