import json

__file_name = 'registered_users.json'  # Nombre del archivo donde se guardarán los usuarios registrados

#metodo en el que se añadirá la lógica de registro de usuarios,
def register_user(*, user:dict):
    if _search_user(username=user['username']):  # Si el usuario ya existe, no se puede registrar
        return False
    else:
        _save_user(user=user) # Guardar el usuario en el archivo
        return True

#Metodo en el que se añadirá la logica de inicio de sesión
def login_user(*, username:str, password:str):
    pass

def _search_user(*, username:str):
    try:
        with open(__file_name, 'r') as file: #Cargar en memoria los usuarios
            usuarios = json.load(file)
            for user in usuarios: #Buscar el usuario por su nombre de usuario

                if user['username'] == username: #Si el nombre de usuario coincide, devolver el usuario
                    return user
    except FileNotFoundError: #Si el archivo no existe, devolver None
        return None

def _save_user(*, user:dict):
    try:
        with open(__file_name, 'r') as file: #Cargar en memoria los usuarios
            usuarios = json.load(file)
    except FileNotFoundError:
        usuarios = []

    usuarios.append(user) #Añadir el nuevo usuario a la lista

    with open(__file_name, 'w') as file:
        json.dump(usuarios, file, indent=4) #Guardar la lista de usuarios actualizada