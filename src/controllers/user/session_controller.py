#
# MANEJO DE REGISTRO DE USUARIO, GUARDARLO EN ARCHIVOS .JSON
# BUSQUEDA Y LOGIN DE USUARIO
#

import json
from src.controllers.user.user_controller import password_is_secure, create_user
from src.utils.encrypter import compare_hashed
from src.enums.register_cases import RegisterCases

from src.enums.access_level import AccessLevel
from src.models.users.user import User
from src.utils.config import REGISTERED_USERS_PATH

#metodo en el que se añadirá la lógica de registro de usuarios,
def register_user(new_user:User) -> RegisterCases:
    #Valida que el nombre de usuario y contraseña no esten vacios
    if not new_user.username or not new_user.password:
        return RegisterCases.EMPTY_INPUT

    if not password_is_secure(new_user.password):
        return RegisterCases.INVALID_PASSWORD

    if _username_is_taken(username=new_user.username):  # Si el usuario ya existe, no se puede registrar
        return RegisterCases.USERNAME_TAKEN
    else:
        _save_new_user(new_user) # Guardar el usuario en el archivo
        return RegisterCases.CORRECT

#Metodo en el que se añadirá la logica de inicio de sesión
def login_user(*, username:str, password:str):
    """Metodo encargado del proceso de login, retorna un objeto usuario en caso de un proceso exitoso, por el contrario, retornará None"""
    try:
        with open(REGISTERED_USERS_PATH, 'r') as file:
            users = json.load(file)
            for usr in users: #Iterar entre todos los usuarios registrados
                if usr['username'] == username:
                    if compare_hashed(usr['password'], password): #Compara las contraseñas encriptadas
                        return create_user(
                            username= usr['username'],
                            password= usr['password'],
                            email=usr['email'],
                            access_level= AccessLevel.from_string(usr['access_level']),
                        )
            return None
    except FileNotFoundError:
        return None

def _username_is_taken(*, username:str):
    """Recibe un username e indica si existe algún usuario registrado con este mismo nombre de usuario"""
    try:
        with open(REGISTERED_USERS_PATH, 'r') as file: #Cargar en memoria los usuarios
            usuarios = json.load(file)
            for user in usuarios: #Buscar el usuario por su nombre de usuario
                if user['username'] == username: #Si el nombre de usuario coincide, devolver el usuario
                    return True
    except FileNotFoundError: #Si el archivo no existe, devolver None
        return False
    return False

def _save_new_user(new_user:User):
    """Recibe un usuario y lo guarda en el archivo local que los almacena"""
    saved_users = []
    try:
        with open(REGISTERED_USERS_PATH, 'r') as file: #Cargar en memoria los usuarios
            saved_users = json.load(file)
    except FileNotFoundError:
        saved_users = []

    saved_users.append(new_user.to_dict()) #Añadir el nuevo usuario a la lista

    with open(REGISTERED_USERS_PATH, 'w') as file:
        json.dump(saved_users, file, indent=4) #Guardar la lista de usuarios actualizada

if __name__ == '__main__': #Prueba cerrada
    user = create_user(
        username='test_user',
        password='Casco12345$',
        email='testing@mail.com',
        access_level= AccessLevel.TECHNICIAN
    )
    print(type(user)) #Mostrar el tipo de objeto del usuario
    print(user.to_dict()) #Mostrar sus datos en forma de diccionario
    print(register_user(user)) #Mostrar que el registro arroje casos correctos
    usr = login_user(username=user.username, password='Casco12345$')
    print(type(usr)) #Mostrar que el login se haga exitosamente
    if usr is None:
        print('not logged')
    else:
        print('logged in')

