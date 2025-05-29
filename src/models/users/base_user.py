from abc import ABC, abstractmethod
from enum import Enum

#clase abstracta usuario, de aqui deberia derivar el ingeniero, supervisor y administrador
#al ser abstracta, no se puede crear un "usuario" pero si sus derivados "ingeniero", "supervisor", etc
class User(ABC):
    def __init__(self, name:str, password:str, email:str):
        self.name = name
        self.email = email
        self.password = password
        self.access_level = self.define_access_level()

    @abstractmethod
    def define_access_level(self) -> Enum:
        #Este metodo debe ser definido para cada usuario para asignar su nivel en jerarquia
        pass