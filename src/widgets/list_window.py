import flet as ft
from src.controllers.equipment_controller import get_all_equipments, get_equipment
from src.controllers.sql.equipment_sql import EquipmentSQL
from src.controllers.sql.user_sql import UserSQL
from src.enums.access_level import AccessLevel

from src.consts.colors import *

def list_window(text: str, page: ft.Page, list_type: str = "equipment", on_select=None, multi_select: bool = False) -> ft.AlertDialog:
    selected_id = None
    selected_ids = set() if multi_select else None
    item_list = ft.ListView(height=300)
    
    def select_item(item_id):
        nonlocal selected_id
        if multi_select:
            if item_id in selected_ids:
                selected_ids.remove(item_id)
            else:
                selected_ids.add(item_id)
        else:
            selected_id = item_id
        update_list(search_bar.value)
        print(f'Seleccionado: {item_id if not multi_select else list(selected_ids)}')
    
    def update_list(search_text=""):
        item_list.controls.clear()
        
        if list_type == "equipment":
            with EquipmentSQL() as db:
                items = db.get_by_partial_name(search_text)
            
            for item in items:
                is_selected = (selected_id == item['code']) if not multi_select else (item['code'] in selected_ids)
                item_list.controls.append(
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.PRECISION_MANUFACTURING),
                        title=ft.Text(item['name']),
                        subtitle=ft.Text(f"Código: {item['code']} - {item['description']}"),
                        trailing=ft.Icon(ft.Icons.CHECK if is_selected else ft.Icons.ARROW_FORWARD_IOS),
                        bgcolor=ft.Colors.BLUE_100 if is_selected else None,
                        on_click=lambda e, code=item['code']: select_item(code)
                    )
                )
        
        elif list_type == "technician":
            with UserSQL() as db:
                items = db.fetch_by_access_level(AccessLevel.TECHNICIAN)
                if search_text:
                    items = [item for item in items if search_text.lower() in item['fullname'].lower()]
            
            for item in items:
                is_selected = (selected_id == item['id']) if not multi_select else (item['id'] in selected_ids)
                item_list.controls.append(
                    ft.ListTile(
                        leading=ft.CircleAvatar(
                            content= ft.Icon(ft.Icons.PERSON),
                            bgcolor= middle_color,
                            color= ft.Colors.WHITE
                            ),

                        title=ft.Text(item['fullname']),
                        subtitle=ft.Text(f"Email: {item['email']}"),
                        trailing=ft.Icon(ft.Icons.CHECK if is_selected else ft.Icons.ARROW_FORWARD_IOS),
                        bgcolor=ft.Colors.BLUE_100 if is_selected else None,
                        on_click=lambda e, user_id=item['id']: select_item(user_id)
                    )
                )
        
        page.update()
    
    search_bar = ft.TextField(
        hint_text="Buscar por nombre ...",
        prefix_icon=ft.Icons.SEARCH,
        width=300,
        border_radius=ft.border_radius.all(30),
        border_color=ft.Colors.GREY_300,
        on_change=lambda e: update_list(e.control.value)
    )
    
    update_list()

    dialog = ft.AlertDialog(
        title=ft.Text(text),
        content=ft.Container(
            width=400,
            height=400,
            content=ft.Column(
                controls=[
                    search_bar,
                    item_list
                ]
            )
        ),
        actions=[
            ft.ElevatedButton(
                "Seleccionar",
                on_click=lambda e: confirm_selection(),
                bgcolor= middle_color,
                color = ft.Colors.WHITE,
                width=100
            ),
            ft.ElevatedButton(
                "Cerrar",
                on_click=lambda e: close_dialog(),
                bgcolor= ft.Colors.RED_300,
                color = ft.Colors.WHITE,
                width=100
            )
        ]
    )
    
    def close_dialog():
        dialog.open = False
        page.update()
    
    def confirm_selection():
        if on_select:
            if multi_select:
                on_select(list(selected_ids))
            else:
                on_select(selected_id)
        close_dialog()
    
    return dialog