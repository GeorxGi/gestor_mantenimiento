from enum import Enum

class AccessLevel(Enum):
    USER = 0
    TECHNICIAN = 1
    SUPERVISOR = 2
    ADMIN = 10

    @classmethod
    def from_string(cls, value: str):
        return cls[value.upper()]