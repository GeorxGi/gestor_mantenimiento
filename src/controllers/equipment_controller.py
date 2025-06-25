from src.controllers.sql.equipment_sql import EquipmentSQL
from src.models.equipment import Equipment

def create_equipment(*, code:str, name:str, description:str, provider:str) -> bool:
    if not code or not name or not description or not provider:
        return False

    is_valid_code = len(code) == 6 and code.isalnum()
    if not is_valid_code:
        return False

    with EquipmentSQL() as db:
        return db.create_equipment(
            code= code,
            name=name,
            description=description,
            provider=provider
        )

def equipment_exists(equipment_code:str) -> bool:
    with EquipmentSQL() as db:
        return True if db.fetch_equipment_data(equipment_code) else False

def get_equipment(equipment_code:str) -> Equipment | None:
    with EquipmentSQL() as db:
        value = db.fetch_equipment_data(equipment_code)
        return Equipment.from_dict(value) if value else None

if __name__ == '__main__':
    print(equipment_exists("a16ebe3c-3efe-43ac-817a-15a83ef54e04"))

    equip = get_equipment("c5bdd09a-807b-4dbe-897d-1461090493d3")
    print(f"{equip.name} - {equip.description} - {equip.provider} - {equip.code}")