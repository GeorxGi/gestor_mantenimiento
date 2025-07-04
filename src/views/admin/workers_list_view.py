import flet as ft
from src.controllers.user.user_controller import get_all_workers
from src.consts.colors import purple_color, dark_grey_color, middle_color, grey_color

def workers_list_view(page: ft.Page):
    """Vista para mostrar la lista de todos los trabajadores (solo para administradores)"""
    
    # Obtener todos los trabajadores
    workers = get_all_workers()
    
    def create_worker_card(worker):
        """Crea una tarjeta para mostrar información del trabajador"""
        
        # Determinar color e icono según el nivel de acceso
        if worker.get_access_level().name == "ADMIN":
            role_color = ft.Colors.RED
            role_icon = ft.Icons.ADMIN_PANEL_SETTINGS
            role_text = "Administrador"
        elif worker.get_access_level().name == "SUPERVISOR":
            role_color = purple_color
            role_icon = ft.Icons.SUPERVISOR_ACCOUNT
            role_text = "Supervisor"
        else:  # TECHNICIAN
            role_color = middle_color
            role_icon = ft.Icons.BUILD
            role_text = "Técnico"
        
        # Estado de asignación para técnicos
        status_text = ""
        status_color = ft.Colors.GREEN
        if hasattr(worker, 'assigned_maintenance_id') and worker.assigned_maintenance_id:
            status_text = "Asignado"
            status_color = ft.Colors.ORANGE
        elif worker.get_access_level().name == "TECHNICIAN":
            status_text = "Disponible"
        
        return ft.Card(
            content=ft.Container(
                content=ft.Row([
                    # Icono del rol
                    ft.Container(
                        content=ft.Icon(
                            role_icon,
                            size=35,
                            color=role_color
                        ),
                        bgcolor=ft.Colors.GREY_100,
                        border_radius=12,
                        padding=12,
                        width=60,
                        height=60,
                        alignment=ft.alignment.center
                    ),
                    # Información del trabajador
                    ft.Column([
                        ft.Text(
                            worker.fullname,
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=dark_grey_color
                        ),
                        ft.Text(
                            worker.email,
                            size=14,
                            color=grey_color
                        ),
                        ft.Row([
                            ft.Text(
                                role_text,
                                size=12,
                                color=role_color,
                                weight=ft.FontWeight.BOLD
                            ),
                            ft.Text(
                                status_text,
                                size=12,
                                color=status_color,
                                weight=ft.FontWeight.W_500
                            ) if status_text else ft.Container()
                        ], spacing=10)
                    ], spacing=3, alignment=ft.MainAxisAlignment.CENTER, expand=True)
                ], spacing=15),
                padding=20
            ),
            elevation=2,
            margin=ft.margin.symmetric(vertical=5)
        )
    
    # Crear las tarjetas de trabajadores
    worker_cards = [create_worker_card(worker) for worker in workers]
    
    # Si no hay trabajadores
    if not worker_cards:
        worker_cards = [
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.PEOPLE_OUTLINE, size=60, color=ft.Colors.GREY_400),
                    ft.Text("No hay trabajadores registrados", size=16, color=ft.Colors.GREY_500)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                padding=40,
                alignment=ft.alignment.center
            )
        ]
    
    return ft.Column(
        controls=[
            # Título
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.PEOPLE, color=purple_color, size=28),
                    ft.Text(
                        "Lista de Trabajadores",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=dark_grey_color
                    )
                ], spacing=10),
                padding=ft.padding.only(bottom=20)
            ),
            # Lista de trabajadores
            ft.Column(
                controls=worker_cards,
                spacing=10,
                scroll=ft.ScrollMode.AUTO,
                expand=True
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
        expand=True
    )