import flet as ft

from src.enums.access_level import AccessLevel
from src.models.users.technician import Technician
from src.utils.session_handler import logout
from src.controllers.maintenance_controller import get_maintenance_basic_info
from src.controllers.user.user_controller import get_user_by_id

def profile_set(page: ft.Page) -> ft.Container:
    user_data = page.session.get("local_user") or {}

    local_user = get_user_by_id(user_data.get("id", ""))
    maintenance_info: dict | None = None

    if isinstance(local_user, Technician):
        maintenance_info = get_maintenance_basic_info(local_user.assigned_maintenance_id)

    def info_line(label: str, value: str) -> ft.Container:
        return ft.Container(
            alignment= ft.alignment.center_left,
            expand= True,
            margin= 5,
            content= ft.Column(
                horizontal_alignment= ft.CrossAxisAlignment.START,
                spacing=2,
                controls=[
                    ft.Text(
                        label.upper() + ":",
                        weight=ft.FontWeight.BOLD,
                        size=14,
                        color=ft.Colors.BLUE_GREY_600,
                        text_align= ft.TextAlign.LEFT
                    ),
                    ft.Text(
                        value or "N/D",
                        size=16,
                        text_align= ft.TextAlign.LEFT
                    )
                ]
            )
        )

    def badge(access_level: AccessLevel):
        bg_color = {
            AccessLevel.USER: ft.Colors.YELLOW_100,
            AccessLevel.TECHNICIAN: ft.Colors.YELLOW_100,
            AccessLevel.SUPERVISOR: ft.Colors.BLUE_100,
            AccessLevel.ADMIN: ft.Colors.PURPLE_100
        }.get(access_level)

        color_by_access= {
            AccessLevel.USER: ft.Colors.YELLOW_800,
            AccessLevel.TECHNICIAN: ft.Colors.YELLOW_800,
            AccessLevel.SUPERVISOR: ft.Colors.BLUE_800,
            AccessLevel.ADMIN: ft.Colors.PURPLE_800
        }.get(access_level)

        return ft.Container(
            bgcolor=bg_color,
            border_radius=20,
            padding=ft.padding.symmetric(horizontal=12, vertical=4),
            content=ft.Text(access_level.name, size=20, weight=ft.FontWeight.W_700, color=color_by_access)
        )

    grey_band = ft.Container(height=40, bgcolor= ft.Colors.BLUE_GREY_700)

    maintenance_column = ft.Column(
        horizontal_alignment= ft.alignment.center,
        controls= [
            ft.Container(
                alignment= ft.alignment.center,
                content= ft.Text(
                    value= "Mantenimiento pendiente",
                    size= 30,
                    color= ft.Colors.BLUE_GREY_600,
                    text_align= ft.TextAlign.CENTER,
                    weight= ft.FontWeight.W_600,
                )
            ),
            info_line(label= "Equipo", value= maintenance_info.get("equipment_name", "")),
            info_line(label= "Fecha mantenimiento", value= maintenance_info.get("date", "")),
            info_line(label= "Detalles", value= maintenance_info.get("details", "")),
            ft.Divider(),
        ]
    ) if maintenance_info else ft.Container()

    def try_to_logout(_):
        def cancelar(_):
            page.close(dlg)

        def aceptar(_):
            page.close(dlg)
            logout(page)

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("¿Cerrar sesión?"),
            content=ft.Text("Esta acción cerrará tu sesión actual."),
            actions=[
                ft.TextButton(text= "Cancelar", on_click=cancelar),
                ft.TextButton(text= "Aceptar", on_click=aceptar),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        page.open(dlg)  # esto lo monta y lo muestra directamente

    return ft.Container(
        padding=ft.padding.symmetric(horizontal=20, vertical=30),
        alignment= ft.alignment.center,
        content= ft.Container(
            bgcolor=ft.Colors.WHITE,
            border_radius=ft.border_radius.all(20),
            border=ft.border.all(width= 1,color= ft.Colors.GREY_200),
            shadow= ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.3, ft.Colors.BLUE_GREY_900),
                offset=ft.Offset(0, 0),
            ),
            content= ft.Column(
                scroll= ft.ScrollMode.ALWAYS,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5,
                controls=[
                    grey_band,
                    ft.Text(
                        local_user.fullname,
                        theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                    ),
                    ft.Row(
                        alignment= ft.MainAxisAlignment.SPACE_EVENLY,
                        controls= [
                            ft.Stack(
                                alignment= ft.alignment.bottom_center,
                                controls= [
                                    ft.Icon(
                                        name=ft.Icons.ACCOUNT_CIRCLE_ROUNDED,
                                        size=150,
                                        color=ft.Colors.BLUE_GREY_700,
                                    ),
                                    badge(local_user.access_level),
                                ]
                            ),
                            info_line(
                                label= "Correo",
                                value= local_user.email,
                            ),
                        ]
                    ),
                    ft.Divider(),
                    maintenance_column,
                    ft.Button(
                        text= 'Cerrar sesión',
                        height= 50,
                        width= 150,
                        on_click= try_to_logout,
                        icon= ft.Icons.LOGOUT,
                        color= ft.Colors.WHITE,
                        bgcolor= ft.Colors.RED_400
                    ),
                    grey_band,
                ]
            )
        )
    )
