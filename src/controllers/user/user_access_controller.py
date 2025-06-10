from src.models.users import user, admin, technician, supervisor
from src.enums.access_level import AccessLevel
from src.utils.config import REGISTERED_USERS_PATH
import json

def get_user_list_by_access_level(access_level:AccessLevel) -> list:
    found_users = []
    try:
        with open(REGISTERED_USERS_PATH, 'r') as file:
            registered_users = json.load(file)
            for usr in registered_users:
                if AccessLevel.from_string(usr['access_level']) == access_level:
                    found_users.append(usr)
    except FileNotFoundError:
        pass
    return found_users

if __name__ == '__main__':
    us = get_user_list_by_access_level(AccessLevel.ADMIN)
    for value in us:
        print(value)
