from enum import Enum

from src.models.users.user import User
from src.enums.access_level import AccessLevel

class Technician(User):
    def __init__(self, *, assigned_maintenance_id:str = '', working_area:str = '', **kwargs):
        super().__init__(**kwargs)
        self.assigned_maintenance_id:str = assigned_maintenance_id
        self.working_area:str = working_area

    def asign_work(self, work_id:str):
        self.assigned_maintenance_id = work_id

    @classmethod
    def from_dict(cls, data:dict):
        user_instante = super().from_dict(data)

        user_instante.__class__ = cls
        user_instante.working_area = data.get("working_area", "")
        user_instante.assigned_maintenance_id =data.get("assigned_maintenance_id")
        return user_instante

    def to_simple_dict(self) -> dict:
        base = super().to_simple_dict()
        base["assigned_maintenance_id"] = self.assigned_maintenance_id

        return base
    def define_access_level(self) -> Enum:
        return AccessLevel.TECHNICIAN