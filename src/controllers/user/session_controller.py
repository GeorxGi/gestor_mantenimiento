#
# MANEJO DE REGISTRO DE USUARIO, GUARDARLO EN ARCHIVOS .JSON
# BUSQUEDA Y LOGIN DE USUARIO
#

import json
import os.path

from src.controllers.user.user_controller import password_is_secure, _create_user_from_dict, is_valid_mail
from src.utils.encrypter import compare_hashed
from src.enums.register_cases import RegisterCases

from src.enums.access_level import AccessLevel
from src.models.users.user import User
from src.utils.config import REGISTERED_USERS_PATH

def read_users():
    try:
        with open(REGISTERED_USERS_PATH, 'r') as file:
            for user in json.load(file):
                yield user
    except (json.JSONDecodeError, FileNotFoundError):
        return

#metodo en el que se añadirá la lógica de registro de usuarios,
def register_user(*, fullname:str, username:str, password:str, email: str, access_level:AccessLevel) -> RegisterCases:
    """Recibe los datos de un usuario, y si todas las validaciones son correctas,
    lo almacena localmente, si no, retorna un enum RegisterCase con el error ocurrido"""
    #Valida que el nombre de usuario y contraseña no esten vacios
    if not fullname or not username or not password or not email or not access_level:
        return RegisterCases.EMPTY_INPUT

    if not isinstance(access_level, AccessLevel):
        return RegisterCases.INVALID_ACCESS_LEVEL

    if not password_is_secure(password):
        return RegisterCases.INVALID_PASSWORD

    if not is_valid_mail(email):
        return RegisterCases.INVALID_EMAIL

    if _username_is_taken(username):  # Si el usuario ya existe, no se puede registrar
        return RegisterCases.USERNAME_TAKEN

    user_dict = {
        "fullname": fullname,
        "username": username,
        "password": password,
        "email": email,
        "access_level": access_level.name
    }
    new_user = _create_user_from_dict(user_dict)
    _add_new_user(new_user) # Guardar el usuario en el archivo
    return RegisterCases.CORRECT

#Metodo en el que se añadirá la logica de inicio de sesión
def login_user(*, username:str, password:str):
    """Metodo encargado del proceso de login,
    retorna un objeto usuario en caso de un proceso exitoso,
    por el contrario, retornará None"""
    for user in read_users():
        if user["username"] != username:
            continue
        else:
            if compare_hashed(user["password"], password):
                return _create_user_from_dict(user)
            else:
                break
    return None

def _username_is_taken(username:str):
    """Recibe un username e indica si existe algún usuario registrado con este mismo nombre de usuario"""
    for user in read_users():
        if user["username"] == username:
            return True
    return False

def _add_new_user(new_user:User):
    """Recibe un usuario y lo guarda en el archivo local que los almacena"""
    try:
        if not os.path.exists(REGISTERED_USERS_PATH):
            with open(REGISTERED_USERS_PATH, 'w') as file:
                json.dump([], file, indent= 4)

        with open(REGISTERED_USERS_PATH, 'r+') as file: #Cargar en memoria los usuarios
            saved_users = json.load(file)
            saved_users.append(new_user.to_dict())
            file.seek(0)
            json.dump(saved_users, file, indent= 4)
            file.truncate()
            return True
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return False

def _update_user(user_id:str, new_value:dict):
    try:
        with open(REGISTERED_USERS_PATH, 'r') as file:
            saved_users = json.load(file)
            user_found = False
            for usr in saved_users:
                if usr.get("id", "") == user_id:
                    for key, value in new_value.items():
                        if key in usr and key not in {"id", "password"}:
                            usr[key] = value
                            user_found = True
                            break
            if user_found:
                with open(REGISTERED_USERS_PATH, "w") as file:
                    json.dump(saved_users, file, indent=4)
                    return True
            return False
    except FileNotFoundError:
        return False

if __name__ == '__main__': #Prueba cerrada
    print(register_user(
        username= 'test_user',
        password= 'Clavesegura123',
        access_level= AccessLevel.TECHNICIAN,
        fullname= 'El Usuario Que Lo Prueba',
        email= 'correoPaProbar@gmail.com',
    ))

    user = login_user(username='UsuarioPrueba1',password='Clavesegura123')

    if user is not None:
        print(_update_user(user_id= user.id, new_value={"username": 'test_user'}))

    if user is None:
        print('Registrando usuario')
        print(  register_user(
                    fullname= 'Usuario Prueba Ramirez',
                    username= 'usr',
                    password= 'Casco12345$',
                    email= 'testing@mail.com',
                    access_level= AccessLevel.TECHNICIAN,
        ))
    else:
        print('Usuario existe')
        print(type(user))
        print(user.to_dict())