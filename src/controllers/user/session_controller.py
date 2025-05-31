#
# MANEJO DE REGISTRO DE USUARIO, GUARDARLO EN ARCHIVOS .JSON
# BUSQUEDA Y LOGIN DE USUARIO
#

import json
from src.utils.encrypter import compare_hashed

from src.enums.access_level import AccessLevel
from src.models.users.user import User
from src.models.users.admin import Admin
from src.models.users.technician import Technician
from src.models.users.supervisor import Supervisor

__file_name = 'registered_users.json'  # Nombre del archivo donde se guardarán los usuarios registrados

#metodo en el que se añadirá la lógica de registro de usuarios,
def register_user(new_user:User):
    if _search_user(username=new_user.username):  # Si el usuario ya existe, no se puede registrar
        return False
    else:
        _save_new_user(new_user) # Guardar el usuario en el archivo
        return True

#Metodo en el que se añadirá la logica de inicio de sesión
def login_user(*, username:str, password:str):
    try:
        with open(__file_name, 'r') as file:
            users = json.load(file)
            for usr in users: #Iterar entre todos los usuarios registrados
                if usr['username'] == username:
                    if compare_hashed(usr['password'], password): #Compara las contraseñas encriptadas
                        return _create_user(
                            username= usr['username'],
                            password= usr['password'],
                            email=usr['email'],
                            access_level= AccessLevel.from_string(usr['access_level']),
                        )
            return None
    except FileNotFoundError:
        return None

def _search_user(*, username:str):
    try:
        with open(__file_name, 'r') as file: #Cargar en memoria los usuarios
            usuarios = json.load(file)
            for user in usuarios: #Buscar el usuario por su nombre de usuario
                if user['username'] == username: #Si el nombre de usuario coincide, devolver el usuario
                    return user

        return None
    except FileNotFoundError: #Si el archivo no existe, devolver None
        return None

def _save_new_user(new_user:User):
    try:
        with open(__file_name, 'r') as file: #Cargar en memoria los usuarios
            saved_users = json.load(file)
    except FileNotFoundError:
        saved_users = []

    saved_users.append(new_user.to_dict()) #Añadir el nuevo usuario a la lista

    with open(__file_name, 'w') as file:
        json.dump(saved_users, file, indent=4) #Guardar la lista de usuarios actualizada

def _create_user(*, username:str, password:str, email:str, access_level:AccessLevel):
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
        case _:
            return None

if __name__ == '__main__': #Prueba cerrada
    user = _create_user(
        username='test_user',
        password='12345',
        email='testing@mail.com',
        access_level= AccessLevel.TECHNICIAN
    )
    print(type(user))
    print(user.to_dict())
    usr = login_user(username=user.username, password='12345')
    print(type(usr))
    if usr is None:
        print('not logged')
    else:
        print('logged in')

