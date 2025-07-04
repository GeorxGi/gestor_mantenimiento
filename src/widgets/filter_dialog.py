import flet as ft

def filter_dialog(page: ft.Page, on_filter_change):
    
    selected_filter = ft.Ref[str]()
    selected_filter.current = "pieces"
    
    def on_radio_change(e):
        selected_filter.current = e.control.value
    
    def apply_filter(e):
        pieces = selected_filter.current == "pieces"
        equipment = selected_filter.current == "equipment"
        maintenance = selected_filter.current == "maintenance"
        on_filter_change(pieces, equipment, maintenance)
        page.close(dialog)
    
    dialog = ft.AlertDialog(
        title=ft.Text("Filtrar por tipo", size=18, weight=ft.FontWeight.BOLD),
        content=ft.Column([
            ft.RadioGroup(
                content=ft.Column([
                    ft.Radio(value="pieces", label="Piezas"),
                    ft.Radio(value="equipment", label="Equipos"),
                    ft.Radio(value="maintenance", label="Órdenes de mantenimiento")
                ]),
                value="pieces",
                on_change=on_radio_change
            )
        ], tight=True, spacing=10),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: page.close(dialog)),
            ft.TextButton("Aplicar", on_click=apply_filter)
        ]
    )
    page.open(dialog)