import flet as ft

def profile_set(page: ft.Page) -> ft.Container:
    user_data = page.session.get("local_user") or {}
    user_fullname = user_data.get("fullname", "")
    user_email = user_data.get("email", "")
    user_access_level = user_data.get("access_level", "")

    def info_line(label: str, value: str) -> ft.Container:
        return ft.Container(
            alignment= ft.alignment.center_left,
            expand= True,
            margin= 10,
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

    def badge(text: str, bgcolor=ft.Colors.BLUE_100, color=ft.Colors.BLUE_800):
        return ft.Container(
            bgcolor=bgcolor,
            border_radius=20,
            padding=ft.padding.symmetric(horizontal=12, vertical=4),
            content=ft.Text(text, size=20, weight=ft.FontWeight.W_700, color=color)
        )

    grey_band = ft.Container(height=40, bgcolor= ft.Colors.BLUE_GREY_700, expand= True)


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
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    grey_band,
                    ft.Column(
                        spacing= 0,
                        alignment= ft.alignment.center,
                        horizontal_alignment= ft.alignment.center,
                        controls= [
                            ft.Icon(
                                name=ft.Icons.ACCOUNT_CIRCLE_ROUNDED,
                                size=150,
                                color=ft.Colors.BLUE_GREY_700,
                            ),
                            badge(user_access_level),
                        ]
                    ),
                    ft.Divider(),
                    ft.Text(
                        user_fullname,
                        style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                    ),
                    ft.Divider(),
                    info_line(label= "Correo", value= user_email),
                    grey_band,
                ]
            )
        )
    )
