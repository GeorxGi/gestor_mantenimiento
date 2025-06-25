#
# MANEJO DE REGISTRO DE USUARIO, GUARDARLO EN ARCHIVOS .JSON
# BUSQUEDA Y LOGIN DE USUARIO
#
from src.controllers.sql.user_sql import UserSQL
from src.controllers.user.user_controller import password_is_secure, _create_user_from_dict, is_valid_mail
from src.utils.encrypter import compare_hashed, hash_password
from src.enums.register_cases import RegisterCases

from src.enums.access_level import AccessLevel

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

    hashed_password = hash_password(password)

    with UserSQL() as db:
        db.create_user(
            username= username,
            password= hashed_password,
            email= email,
            access_level= access_level,
            fullname= fullname
        )
    return RegisterCases.CORRECT

#Metodo en el que se añadirá la logica de inicio de sesión
def login_user(*, username:str, password:str):
    """Metodo encargado del proceso de login,
    retorna un objeto usuario en caso de un proceso exitoso,
    por el contrario, retornará None"""
    if not username or not password:
        return None

    with UserSQL() as db:
        login_user_data = db.login_fetch(username)

    if not login_user_data:
        return None

    user_password = login_user_data.get("password", "")
    if not compare_hashed(password, user_password):
        return None
    with UserSQL() as db:
        logged_user = db.fetch_by_username(username)
    return _create_user_from_dict(logged_user)

def _username_is_taken(username:str) -> bool:
    """Recibe un username e indica si existe algún usuario registrado con este mismo nombre de usuario"""
    with UserSQL() as db:
        return True if db.fetch_by_username(username) else False

if __name__ == '__main__': #Prueba cerrada
    print(register_user(
        username= 'test_user',
        password= 'Clavesegura123',
        access_level= AccessLevel.TECHNICIAN,
        fullname= 'El Usuario Que Lo Prueba',
        email= 'correoPaProbar@gmail.com',
    ).value)

    user = login_user(username='test_user',password='Clavesegura123')

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