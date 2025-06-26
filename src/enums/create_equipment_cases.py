from enum import Enum

class CreateEquipmentCases(Enum):
    CORRECT = 'Equipo registrado exitosamente'
    EMPTY_INPUT = 'Rellene todos los campos necesarios'
    CODE_TAKEN = 'El código ingresado está ocupado'
    NOT_VALID_CODE = 'El código ingresado debe tener una longitud de 6 y ser alfanumérico'
