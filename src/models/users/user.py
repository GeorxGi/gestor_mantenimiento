from abc import ABC, abstractmethod
from enum import Enum
from src.utils.encrypter import hash_password
import uuid

#clase abstracta usuario, de aqui deberia derivar el ingeniero, supervisor y administrador
#al ser abstracta, no se puede crear un "usuario" pero si sus derivados "ingeniero", "supervisor", etc
class User(ABC):
    def __init__(self, *,  fullname:str, username:str, password:str, email:str, id:str = ''):
        self.id = id if id else str(uuid.uuid4())
        self.fullname = fullname
        self.username = username
        self.password = hash_password(password)
        self.email = email
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

    @classmethod
    def from_dict(cls, data:dict):
        return cls(
            id=data.get("id", ""),
            fullname=data.get("fullname", ""),
            username=data.get("username", ""),
            password=data.get("password", ""),
            email=data.get("email", ""),
        )