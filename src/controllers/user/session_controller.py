#
# MANEJO DE REGISTRO DE USUARIO, GUARDARLO EN ARCHIVOS .JSON
# BUSQUEDA Y LOGIN DE USUARIO
#
from src.controllers.datafile_controller import DataFileController
from src.controllers.user.user_controller import password_is_secure, _create_user_from_dict, is_valid_mail
from src.utils.encrypter import compare_hashed, hash_password
from src.enums.register_cases import RegisterCases

from src.enums.access_level import AccessLevel

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
        "password": hash_password(password),
        "email": email,
        "access_level": access_level.name
    }
    new_user = _create_user_from_dict(user_dict)
    DataFileController.add_new_user(new_user.to_dict()) # Guardar el usuario en el archivo
    return RegisterCases.CORRECT

#Metodo en el que se añadirá la logica de inicio de sesión
def login_user(*, username:str, password:str):
    """Metodo encargado del proceso de login,
    retorna un objeto usuario en caso de un proceso exitoso,
    por el contrario, retornará None"""
    for user in DataFileController.read_users():
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
    for user in DataFileController.read_users():
        if user["username"] == username:
            return True
    return False

if __name__ == '__main__': #Prueba cerrada
    print(register_user(
        username= 'test_user',
        password= 'Clavesegura123',
        access_level= AccessLevel.TECHNICIAN,
        fullname= 'El Usuario Que Lo Prueba',
        email= 'correoPaProbar@gmail.com',
    ).value)

    user = login_user(username='UsuarioPrueba1',password='Clavesegura123')

    if user is None:
        print('Registrando usuario')
        print(register_user(
                fullname= 'Usuario Prueba Ramirez',
                username= 'usr',
                password= 'Casco123',
                email= 'testing@mail.com',
                access_level= AccessLevel.TECHNICIAN,
        ).value)
    else:
        print('Usuario existe')
        print(type(user))
        print(user.to_dict())