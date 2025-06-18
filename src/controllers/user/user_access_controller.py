from src.enums.access_level import AccessLevel
from src.controllers.datafile_controller import DataFileController
from src.controllers.user.session_controller import _create_user_from_dict

def get_user_list_by_access_level(access_level:AccessLevel) -> list[dict]:
    """Recibe un access_level y retorna una lista de diccionarios con datos básicos de
    los usuarios encontrados con este mismo access_level"""
    found_users = []
    for usr in DataFileController.read_users():
        if AccessLevel.from_string(usr.get("access_level", "")) == access_level:
            found = _create_user_from_dict(usr)

            found_users.append(found.to_simple_dict())
    return found_users

def get_not_busy_technicians() -> list[str]:
    found_tech = []
    for tech in DataFileController.read_users_by_access_level(AccessLevel.TECHNICIAN):
        if tech.get("asigned_work_id", "") == "":
            found = _create_user_from_dict(tech)

            found_tech.append(found.to_simple_dict())
    return found_tech

if __name__ == '__main__':
    us = get_not_busy_technicians()
    for value in us:
        print(value)
