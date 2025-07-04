import flet as ft
from src.controllers.user.user_controller import get_users_by_partial_name


def worker_list(page: ft.Page):
     data= [
        ft.ListTile(
        leading= ft.Icon(ft.Icons.ACCOUNT_CIRCLE_ROUNDED, color= ft.Colors.GREEN_600),
        title= ft.Text(value= f"{user.fullname}", weight= ft.FontWeight.BOLD),
        subtitle= ft.Text(user.access_level.name),
        on_click= None
        ) for user in get_users_by_partial_name('')
    ]
     return ft.ListView(
         controls=data,
         spacing= 10,
     )