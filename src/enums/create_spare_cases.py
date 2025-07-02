from enum import Enum

class CreateSpareCases(Enum):
    CORRECT = "Pieza registrada exitosamente"
    EMPTY_INPUT = "Rellene todos los campos"
    INVALID_AMOUNT = "La cantidad ingresada debe ser igual o mayor a 0"
    INVALID_IMAGE = "La imágen ingresada no es compatible"
    UNKNOWN_ERROR = "Ocurrió un error inesperado..."