from enum import Enum

class RegisterCases(str, Enum):
    CORRECT = "Registro realizado exitosamente",
    INVALID_PASSWORD = "Contraseña no válida",
    INVALID_EMAIL = "Correo no válido",
    INVALID_ACCESS_LEVEL = "Nivel de acceso no existente/válido",
    USERNAME_TAKEN = "Nombre de usuario ocupado",
    EMAIL_TAKEN = "Correo electrónico ocupado",
    EMPTY_INPUT = "Rellene los campos",

if __name__ == '__main__':
    print(RegisterCases.CORRECT.value)
    print(RegisterCases.CORRECT)
