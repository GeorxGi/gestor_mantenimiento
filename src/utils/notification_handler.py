from src.enums.access_level import AccessLevel
import flet as ft

from src.widgets.custom_snack_bar import custom_snack_bar

listening_sessions = {}

def notify_supervisors(event:str, content:str):
    for session in listening_sessions.values():
        if session["access_level"] == AccessLevel.SUPERVISOR.name:
            session["page"].pubsub.send_all({
                "event": event,
                "content": content
            })

def notify_admins(event:str, content:str):
    for session in listening_sessions.values():
        if session["access_level"] == AccessLevel.ADMIN.name:
            session["page"].pubsub.send_all({
                "event": event,
                "content": content
            })

def listen_to(page: ft.Page, user_id:str, access_level:AccessLevel):
    listening_sessions[page.session_id] = {
        "page": page,
        "user_id": user_id,
        "access_level": access_level.name
    }
    def receipt(msg):
        event = msg.get("event")
        if event == "new_equipment":
            content = msg.get("content")
            page.open(custom_snack_bar(content= content))
            page.update()

    page.pubsub.subscribe(receipt)