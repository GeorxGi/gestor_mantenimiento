from enum import Enum

class CreateMaintenanceCases(str, Enum):
    CORRECT = "Mantenimiento creado exitosamente"
    EMPTY_IMPUT = "Rellene los campos indicados"
    BUSY_TECHNICIAN = "Uno de los técnicos ingresados se encuentra ocupado"
    NOT_VALID_DATE = "Fecha de mantenimiento no válida"
    NOT_REGISTERED_ID = "Hubo un problema al verificar al supervisor o técnicos"
    EQUIPMENT_NOT_FOUND = "El ID del equipo ingresado no pudo ser encontrado"
    EQUIPMENT_ALREADY_HAS_MAINTENANCE = "El equipo indicado ya posee un mantenimiento pendiente"
    SUPERVISOR_ID_IS_NOT_SUPERVISOR = 'El usuario ingresado como "supervisor" no está registrado como supervisor'
    TECHNICIAN_ID_IS_NOT_TECHNICIAN = 'El usuario ingresado como "técnico" no está registrado como técnico'
