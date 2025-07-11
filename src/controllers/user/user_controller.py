#
# LOGICA CON EL MANEJO DE USUARIOS
# * verificar nivel de acceso, entre otro
#
import re

from src.enums.access_level import AccessLevel
from src.models.users.admin import Admin
from src.models.users.technician import Technician
from src.models.users.supervisor import Supervisor
from src.models.users.user import User

from src.controllers.sql.user_sql import UserSQL

def get_user_by_id(user_id:str) -> Technician | Supervisor | Admin | None:
    with UserSQL() as db:
        data = db.fetch_user_by_id(user_id)
        return _create_user_from_dict(data)

def get_users_by_partial_name(partial_name:str) -> list[Technician | Supervisor | Admin]:
    with UserSQL() as db:
        if not partial_name:
            data = db.fetchall_users()
        else:
            data = db.fetchall_users_by_partial_name(partial_name)
        return [_create_user_from_dict(user) for user in data]

def get_all_available_technicians() -> list[Technician]:
    with UserSQL() as db:
        data = db.fetch_available_technicians()
        print(data)
        return [Technician.from_dict(tech) for tech in data]

def check_access_level(user:User):
    return user.get_access_level()

def password_is_secure(password:str) -> bool:
    """Recibe un string y retorna un booleano que indica si la cadena representa
    una contraseña que cumpla los requisitos de seguridad"""
    has_number = False
    has_mayus = False

    if len(password) < 4: #Contraseña mayor a 4 caracteres
        return False
    else:
        for char in password:
            if not has_mayus and char.isupper():
                has_mayus = True
            if not has_number and  char.isnumeric():
                has_number = True
        is_valid_pass = has_mayus and has_number
        return is_valid_pass

def is_valid_mail(email:str) -> bool:
    """Recibe un string y retorna un booleano que indica si la cadena representa
    un correo elecronico valido"""
    #cadena Regex tomada de internet, muchas ganas intentar entender esto
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.fullmatch(email_regex, email):
        return True
    return False

def _create_user_from_dict(user_dict:dict) -> Technician | Supervisor | Admin | None:
    """Crea una instancia de usuario en base a los datos ingresados"""
    match AccessLevel.from_string(str(user_dict.get("access_level", ""))):
        case AccessLevel.TECHNICIAN:
            return Technician.from_dict(user_dict)
        case AccessLevel.SUPERVISOR:
            return Supervisor.from_dict(user_dict)
        case AccessLevel.ADMIN:
            return Admin.from_dict(user_dict)
    return None

#Pruebas unitarias
if __name__ == '__main__':
    data = get_users_by_partial_name('Supe')
    for row in data:
        print(row.fullname)
    #print(is_valid_mail('correo@gmail.com'))
    #print(is_valid_mail('falso@.com'))
    #print(is_valid_mail('correo-seguro@net-star.net'))