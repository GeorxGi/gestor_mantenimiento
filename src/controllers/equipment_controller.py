import sqlite3

from src.controllers.sql.equipment_sql import EquipmentSQL
from src.enums.create_equipment_cases import CreateEquipmentCases
from src.models.equipment import Equipment

def create_equipment(*, code:str, name:str, description:str, provider:str) -> CreateEquipmentCases:
    if not code or not name or not description or not provider:
        return CreateEquipmentCases.EMPTY_INPUT

    is_valid_code = len(code) == 6 and code.isalnum()
    if not is_valid_code:
        return CreateEquipmentCases.NOT_VALID_CODE
    with EquipmentSQL() as db:
        try:
            db.create_equipment(
                code= code.upper(),
                name=name,
                description=description,
                provider=provider
            )
            return CreateEquipmentCases.CORRECT
        except sqlite3.IntegrityError:
            return CreateEquipmentCases.CODE_TAKEN

def equipment_exists(equipment_code:str) -> bool:
    with EquipmentSQL() as db:
        return True if db.fetch_equipment_data(equipment_code.upper()) else False

def get_equipment(equipment_code:str) -> Equipment | None:
    with EquipmentSQL() as db:
        value = db.fetch_equipment_data(equipment_code.upper())
        return Equipment.from_dict(value) if value else None

def get_all_equipments() -> list[Equipment]:
    with EquipmentSQL() as db:
        equipments = db.get_by_partial_name("")
        return [Equipment.from_dict(eq) for eq in equipments]

if __name__ == '__main__':
    print (create_equipment(
        code= '123456',
        name= 'Algo de prueba',
        provider= 'Sansu',
        description= 'Borrar luego'
    ))