from enum import Enum

from src.models.users.user import User
from src.enums.access_level import AccessLevel

class Technician(User):
    def __init__(self, *, working_area:str = '', **kwargs):
        super().__init__(**kwargs)
        self.working_area = working_area

    @classmethod
    def from_dict(cls, data:dict):
        user_instante = super().from_dict(data)

        user_instante.__class__ = cls
        user_instante.working_area = data.get("working_area", "")
        return user_instante

    def define_access_level(self) -> Enum:
        return AccessLevel.TECHNICIAN