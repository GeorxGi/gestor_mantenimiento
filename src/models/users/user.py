from abc import ABC, abstractmethod
from enum import Enum
import uuid

#clase abstracta usuario, de aqui deberia derivar el ingeniero, supervisor y administrador
#al ser abstracta, no se puede crear un "usuario" pero si sus derivados "ingeniero", "supervisor", etc
class User(ABC):
    def __init__(self, *,  fullname:str, username:str, password:str, email:str, id:str = ''):
        self.id:str = id if id else str(uuid.uuid4())
        self.fullname:str = fullname
        self.username:str = username
        self.password:str = password
        self.email:str = email
        self.access_level = self.define_access_level()

    @abstractmethod
    def define_access_level(self) -> Enum:
        #Este metodo debe ser definido para cada usuario para asignar su nivel en jerarquia
        pass

    def get_access_level(self) -> Enum:
        return self.access_level

    def to_dict(self) -> dict:
        data = {key: value for key, value in vars(self).items() if key != "access_level"}
        data["access_level"] = self.access_level.name

        return data

    def to_simple_dict(self):
        """Metodo que retorna un diccionario con datos básicos del usuario,
        para evitar comprometer datos como contraseñas, nombres de usuario, etc"""
        return {
            "id": self.id,
            "fullname": self.fullname,
            "email": self.email,
            "access_level": self.access_level.name,
        }

    @classmethod
    def from_dict(cls, data:dict):
        return cls(
            id=data.get("id", ""),
            fullname=data.get("fullname", ""),
            username=data.get("username", ""),
            password=data.get("password", ""),
            email=data.get("email", ""),
        )