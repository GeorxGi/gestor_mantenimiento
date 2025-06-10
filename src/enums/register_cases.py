from enum import Enum

class RegisterCases(Enum):
    CORRECT = 0,
    INVALID_PASSWORD = 1,
    USERNAME_TAKEN = 2,
    EMPTY_INPUT = 3,
    INVALID_EMAIL = 4,
    INVALID_ACCESS_LEVEL = 5,