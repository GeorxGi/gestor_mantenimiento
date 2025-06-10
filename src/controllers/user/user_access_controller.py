from src.enums.access_level import AccessLevel
from src.utils.config import REGISTERED_USERS_PATH
from src.controllers.user.session_controller import _create_user_from_dict
import json

def get_user_list_by_access_level(access_level:AccessLevel) -> list:
    """Recibe un access_level y retorna una lista de diccionarios con datos básicos de
    los usuarios encontrados con este mismo access_level"""
    found_users = []
    try:
        with open(REGISTERED_USERS_PATH, 'r') as file:
            registered_users = json.load(file)
            for usr in registered_users:
                if AccessLevel.from_string(usr.get("access_level", "")) == access_level:

                    found = _create_user_from_dict(usr) #Crea una instancia del objeto usuario

                    found_users.append(found.to_simple_dict()) #Anexa un diccionario simplificado del usuario
    except FileNotFoundError:
        pass
    return found_users

if __name__ == '__main__':
    us = get_user_list_by_access_level(AccessLevel.TECHNICIAN)
    for value in us:
        print(value)
