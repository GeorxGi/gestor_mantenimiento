from enum import Enum

class RegisterCases(Enum):
    CORRECT = 0,
    INVALID_USERNAME = 1,
    INVALID_PASSWORD = 2,
    USERNAME_TAKEN = 3,
    EMPTY_INPUT = 4,