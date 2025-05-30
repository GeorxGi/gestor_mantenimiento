from abc import ABC, abstractmethod
from enum import Enum
from src.utils.encrypter import hash_password

#clase abstracta usuario, de aqui deberia derivar el ingeniero, supervisor y administrador
#al ser abstracta, no se puede crear un "usuario" pero si sus derivados "ingeniero", "supervisor", etc
class User(ABC):
    def __init__(self, *,  username:str, password:str, email:str):
        self.username = username
        self.email = email
        self.password = password
        self.access_level = self.define_access_level()

    @abstractmethod
    def define_access_level(self) -> Enum:
        #Este metodo debe ser definido para cada usuario para asignar su nivel en jerarquia
        pass

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "email": self.email,
            "password": hash_password(self.password), #Almacena la contraseña de forma encriptada
            "access_level": self.access_level.name
        }