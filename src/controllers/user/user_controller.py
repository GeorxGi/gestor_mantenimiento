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

def check_access_level(user:User):
    return user.get_access_level()

def password_is_secure(password:str) -> bool:
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
    #cadena Regex tomada de internet, muchas ganas intentar entender esto
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.fullmatch(email_regex, email):
        return True
    return False

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

#Pruebas unitarias
if __name__ == '__main__':
    print(is_valid_mail('correo@gmail.com'))
    print(is_valid_mail('falso@.com'))
    print(is_valid_mail('correo-seguro@net-star.net'))