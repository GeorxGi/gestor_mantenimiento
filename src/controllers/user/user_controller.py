#
# LOGICA CON EL MANEJO DE USUARIOS
# * verificar nivel de acceso, entre otro
#

from src.enums.access_level import AccessLevel
from src.models.users.admin import Admin
from src.models.users.technician import Technician
from src.models.users.supervisor import Supervisor
from src.models.users.user import User

def check_access_level(user:User):
    return user.get_access_level()

def password_is_secure(password:str):
    has_number = False
    has_special_char = False
    has_mayus = False

    if len(password) < 4: #Contraseña mayor a 4 caracteres
        return False
    else:
        for char in password:
            if not has_mayus and char.isupper():
                has_mayus = True
            if not has_number and  char.isnumeric():
                has_number = True
            if not has_special_char and char.isalnum():
                has_special_char = True
        is_valid_pass = has_mayus and has_number and has_special_char
        return is_valid_pass

def create_user(*, username:str, password:str, email:str, access_level:AccessLevel):
    match access_level:
        case AccessLevel.TECHNICIAN:
            return Technician(
                username=username,
                password=password,
                email= email,
            )
        case AccessLevel.SUPERVISOR:
            return Supervisor(
                username = username,
                password=password,
                email= email,
            )
        case AccessLevel.ADMIN:
            return Admin(
                username= username,
                password=password,
                email= email,
            )
    return None