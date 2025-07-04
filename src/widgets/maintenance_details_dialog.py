import flet as ft
from src.consts.colors import *

def maintenance_details_dialog(page: ft.Page, maintenance_item: dict):
    
    status_color = ft.Colors.ORANGE if maintenance_item["status"] == "Pendiente" else ft.Colors.GREEN
    status_icon = ft.Icons.SCHEDULE if maintenance_item["status"] == "Pendiente" else ft.Icons.CHECK_CIRCLE
    
    # Icono principal de la orden de mantenimiento
    maintenance_icon = ft.Container(
        width=120,
        height=120,
        bgcolor=ft.Colors.GREY_100,
        border_radius=20,
        border=ft.border.all(2, ft.Colors.GREY_300),
        alignment=ft.alignment.center,
        content=ft.Icon(
            status_icon,
            size=60,
            color=status_color
        )
    )
    
    # Información de la orden con mejor diseño
    info_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.PRECISION_MANUFACTURING, color=dark_grey_color, size=20),
                    ft.Text(f"Equipo: {maintenance_item['equipment_code']}", size=16, weight=ft.FontWeight.BOLD)
                ], spacing=8),
                ft.Row([
                    ft.Icon(ft.Icons.PERSON, color=purple_color, size=20),
                    ft.Text(f"Técnicos: {maintenance_item.get('technicians', 'Sin asignar')}", size=14, weight=ft.FontWeight.W_500, color=purple_color)
                ], spacing=8),
                ft.Row([
                    ft.Icon(ft.Icons.DESCRIPTION, color=middle_color, size=20),
                    ft.Text(maintenance_item["details"], size=14, color=dark_grey_color, expand=True)
                ], spacing=8),
                ft.Row([
                    ft.Icon(ft.Icons.CALENDAR_TODAY, color=grey_color, size=20),
                    ft.Text(f"Fecha: {maintenance_item['date']}", size=14, color=grey_color)
                ], spacing=8),
                ft.Row([
                    ft.Icon(ft.Icons.INFO, color=status_color, size=20),
                    ft.Text(
                        f"Estado: {maintenance_item['status']}",
                        size=14,
                        color=status_color,
                        weight=ft.FontWeight.BOLD
                    )
                ], spacing=8)
            ], spacing=12),
            padding=20,
            width=400
        ),
        elevation=2
    )
    
    # Botones de acción
    action_buttons = ft.Row([
        ft.ElevatedButton(
            text="Editar",
            icon=ft.Icons.EDIT,
            bgcolor=middle_color,
            color=ft.Colors.WHITE,
            on_click=lambda _: edit_maintenance(page, dialog, maintenance_item)
        ),
        ft.ElevatedButton(
            text="Completar" if maintenance_item["status"] == "Pendiente" else "Reabrir",
            icon=ft.Icons.CHECK_CIRCLE if maintenance_item["status"] == "Pendiente" else ft.Icons.REFRESH,
            bgcolor=ft.Colors.GREEN if maintenance_item["status"] == "Pendiente" else ft.Colors.ORANGE,
            color=ft.Colors.WHITE,
            on_click=lambda _: toggle_maintenance_status(page, dialog, maintenance_item)
        ),
        ft.ElevatedButton(
            text="Eliminar",
            icon=ft.Icons.DELETE,
            bgcolor=ft.Colors.RED_400,
            color=ft.Colors.WHITE,
            on_click=lambda _: delete_maintenance_confirm(page, dialog, maintenance_item)
        ),
        ft.OutlinedButton(
            text="Cerrar",
            on_click=lambda _: page.close(dialog)
        )
    ], spacing=8, alignment=ft.MainAxisAlignment.CENTER, wrap=True)
    
    dialog = ft.AlertDialog(
        title=ft.Row([
            ft.Icon(ft.Icons.BUILD, color=status_color),
            ft.Text("Detalles de Mantenimiento", size=20, weight=ft.FontWeight.BOLD)
        ], spacing=10),
        content=ft.Column([
            maintenance_icon,
            ft.Divider(height=20),
            info_card,
            ft.Divider(height=10),
            action_buttons
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
        content_padding=30
    )
    page.open(dialog)

def edit_maintenance(page: ft.Page, current_dialog, maintenance_item: dict):
    equipment_field = ft.Container(
        content=ft.TextField(
            value=maintenance_item["equipment_code"],
            label="Código del equipo",
            prefix_icon=ft.Icons.PRECISION_MANUFACTURING,
            border_radius=15,
            border_color=middle_color,
            focused_border_color=purple_color,
            label_style=ft.TextStyle(color=middle_color),
            text_style=ft.TextStyle(size=16),
            content_padding=ft.padding.symmetric(horizontal=15, vertical=12)
        ),
        width=350,
        padding=ft.padding.all(5)
    )
    details_field = ft.Container(
        content=ft.TextField(
            value=maintenance_item["details"],
            label="Detalles del mantenimiento",
            prefix_icon=ft.Icons.DESCRIPTION,
            multiline=True,
            max_lines=3,
            border_radius=15,
            border_color=middle_color,
            focused_border_color=purple_color,
            label_style=ft.TextStyle(color=middle_color),
            text_style=ft.TextStyle(size=14),
            content_padding=ft.padding.symmetric(horizontal=15, vertical=12)
        ),
        width=350,
        padding=ft.padding.all(5)
    )
    date_field = ft.Container(
        content=ft.TextField(
            value=maintenance_item["date"],
            label="Fecha",
            prefix_icon=ft.Icons.CALENDAR_TODAY,
            border_radius=15,
            border_color=middle_color,
            focused_border_color=purple_color,
            label_style=ft.TextStyle(color=middle_color),
            text_style=ft.TextStyle(size=16),
            content_padding=ft.padding.symmetric(horizontal=15, vertical=12)
        ),
        width=350,
        padding=ft.padding.all(5)
    )
    
    def save_changes(e):
        # Aquí iría la lógica para actualizar la orden de mantenimiento
        page.close(edit_dialog)
        page.close(current_dialog)
        page.snack_bar = ft.SnackBar(content=ft.Text("Orden de mantenimiento actualizada"))
        page.snack_bar.open = True
        page.update()
    
    edit_dialog = ft.AlertDialog(
        title=ft.Row([
            ft.Icon(ft.Icons.EDIT, color=middle_color),
            ft.Text("Editar Mantenimiento", weight=ft.FontWeight.BOLD)
        ], spacing=10),
        content=ft.Column([equipment_field, details_field, date_field], spacing=15, tight=True),
        actions=[
            ft.ElevatedButton(
                text="Guardar",
                icon=ft.Icons.SAVE,
                bgcolor=middle_color,
                color=ft.Colors.WHITE,
                on_click=save_changes
            ),
            ft.OutlinedButton(
                text="Cancelar",
                on_click=lambda _: page.close(edit_dialog)
            )
        ]
    )
    page.open(edit_dialog)

def toggle_maintenance_status(page: ft.Page, current_dialog, maintenance_item: dict):
    new_status = "Completado" if maintenance_item["status"] == "Pendiente" else "Pendiente"
    action = "completar" if maintenance_item["status"] == "Pendiente" else "reabrir"
    
    def confirm_toggle(e):
        # Aquí iría la lógica para cambiar el estado
        page.close(confirm_dialog)
        page.close(current_dialog)
        page.snack_bar = ft.SnackBar(content=ft.Text(f"Mantenimiento {action}do correctamente"))
        page.snack_bar.open = True
        page.update()
    
    confirm_dialog = ft.AlertDialog(
        title=ft.Row([
            ft.Icon(ft.Icons.INFO, color=middle_color),
            ft.Text(f"Confirmar {action.title()}", weight=ft.FontWeight.BOLD)
        ], spacing=10),
        content=ft.Text(f"¿Estás seguro de que quieres {action} esta orden de mantenimiento?"),
        actions=[
            ft.ElevatedButton(
                text=action.title(),
                bgcolor=middle_color,
                color=ft.Colors.WHITE,
                on_click=confirm_toggle
            ),
            ft.OutlinedButton(
                text="Cancelar",
                on_click=lambda _: page.close(confirm_dialog)
            )
        ]
    )
    page.open(confirm_dialog)

def delete_maintenance_confirm(page: ft.Page, current_dialog, maintenance_item: dict):
    def confirm_delete(e):
        # Aquí iría la lógica para eliminar la orden
        page.close(confirm_dialog)
        page.close(current_dialog)
        page.snack_bar = ft.SnackBar(content=ft.Text("Orden de mantenimiento eliminada"))
        page.snack_bar.open = True
        page.update()
    
    confirm_dialog = ft.AlertDialog(
        title=ft.Row([
            ft.Icon(ft.Icons.WARNING, color=ft.Colors.RED_400),
            ft.Text("Confirmar Eliminación", weight=ft.FontWeight.BOLD)
        ], spacing=10),
        content=ft.Column([
            ft.Icon(ft.Icons.DELETE_FOREVER, size=60, color=ft.Colors.RED_300),
            ft.Text(
                f"¿Estás seguro de que quieres eliminar la orden #{maintenance_item['id']}?",
                text_align=ft.TextAlign.CENTER,
                size=16
            ),
            ft.Text(
                "Esta acción no se puede deshacer.",
                text_align=ft.TextAlign.CENTER,
                color=ft.Colors.GREY_600,
                size=12
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10, tight=True),
        actions=[
            ft.ElevatedButton(
                text="Eliminar",
                icon=ft.Icons.DELETE,
                bgcolor=ft.Colors.RED_400,
                color=ft.Colors.WHITE,
                on_click=confirm_delete
            ),
            ft.OutlinedButton(
                text="Cancelar",
                on_click=lambda _: page.close(confirm_dialog)
            )
        ]
    )
    page.open(confirm_dialog)