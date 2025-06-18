import uuid

from src.models.equipment import Equipment
from src.controllers.datafile_controller import DataFileController

def equipment_exist(equipment_id:str) -> bool:
    for equip in DataFileController.read_equipments():
        if equip.get("id") == equipment_id:
            return True
    return False

def create_equipment(*, name:str, description:str, provider:str) -> bool:
    if not name or not description or not provider:
        return False

    new_equipment = Equipment(
        maintenance_id= "",
        name= name,
        description= description,
        provider= provider,
        id= str(uuid.uuid4())
    )
    DataFileController.add_new_equipment(new_equipment.__dict__)

    return True

def asign_maintenance_to_equipment(equipment_id:str, maintenance_id:str) -> bool:
    if not equipment_id or not maintenance_id:
        return False

    for equip in DataFileController.read_equipments():
        if equip.get("id", "") == equipment_id:
            #Valida que el equipo ingresado no tenga un mantenimiento ya registrado
            if equip.get("maintenance_id", "") != "":
                return False

    response = DataFileController.update_equipment(
        equipment_id= equipment_id,
        new_value= maintenance_id,
        key= "maintenance_id"
    )
    return response

if __name__ == '__main__':
    pass