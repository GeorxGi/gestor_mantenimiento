import flet as ft

def custom_snack_bar(*, content:str, bgcolor:ft.Colors = ft.Colors.BLUE) -> ft.SnackBar:
    return ft.SnackBar(
        bgcolor= bgcolor,
        behavior= ft.SnackBarBehavior.FLOATING,
        content= ft.Text(
            value= content,
            color= ft.Colors.WHITE,
        )
    )