from enum import Enum

from base_user import User
from src.enums.access_level import AccessLevel

class Admin(User):
    def define_access_level(self) -> Enum:
        return AccessLevel.ADMIN