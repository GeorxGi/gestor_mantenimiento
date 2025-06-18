#
# CONTROLADOR ENCARGADO DEL MANEJO DE MANTENIMIENTOS
# (Creación, modificación, etc)
#

from datetime import date
import uuid

from src.enums.access_level import AccessLevel
from src.enums.create_maintenance_cases import CreateMaintenanceCases

from src.controllers.datafile_controller import DataFileController
from src.controllers.equipment_controller import equipment_exist, asign_maintenance_to_equipment

from src.models.maintenance import Maintenance

def create_maintenance_order(*, equipment_id:str, supervisor_id:str, asigned_technicians_id:list[str], name:str, details:str, maintenance_date:date) -> CreateMaintenanceCases:
    #Verificia que los datos de entrada no estén vacios
    if not supervisor_id or not asigned_technicians_id or not name or not details or not maintenance_date or not equipment_id:
        return CreateMaintenanceCases.EMPTY_IMPUT

    # Verifica que el id del equipo ingresado exista
    if not equipment_exist(equipment_id):
        return CreateMaintenanceCases.EQUIPMENT_NOT_FOUND

    #Validar que las ID del supervisor y tecnicos ingresados existan y tengan el cargo ingresado
    found_supervisor = False
    tech_counter = len(asigned_technicians_id)

    for user in DataFileController.read_users():
        user_id = user.get("id", "")
        #Validar que sea un supervisor
        if not found_supervisor and user_id == supervisor_id:
            if AccessLevel.from_string(user.get("access_level", "")) == AccessLevel.SUPERVISOR:
                found_supervisor = True
                continue
            else:
                return CreateMaintenanceCases.SUPERVISOR_ID_IS_NOT_SUPERVISOR
        #Validar que sea un técnico
        if user_id in asigned_technicians_id:
            if AccessLevel.from_string(user.get("access_level", "")) == AccessLevel.TECHNICIAN:
                if user.get("asigned_work_id", "") != "":
                    return CreateMaintenanceCases.BUSY_TECHNICIAN
                else:
                    tech_counter = tech_counter - 1
            else:
                return CreateMaintenanceCases.TECHNICIAN_ID_IS_NOT_TECHNICIAN

    if tech_counter != 0 or not found_supervisor:
        return CreateMaintenanceCases.NOT_REGISTERED_ID

    if maintenance_date < date.today():
        return CreateMaintenanceCases.NOT_VALID_DATE

    new_maintenance = Maintenance(
        supervisor_id= supervisor_id,
        maintenance_id= str(uuid.uuid4()),
        asigned_technicians_id=asigned_technicians_id,
        maintenance_date= maintenance_date,
        details= details,
        is_pending= True,
        equipment_id= equipment_id
    )

    if not asign_maintenance_to_equipment(equipment_id, new_maintenance.id):
        return CreateMaintenanceCases.EQUIPMENT_ALREADY_HAS_MAINTENANCE

    for tech in asigned_technicians_id:
        DataFileController.update_user(
            user_id= tech,
            new_value= new_maintenance.id,
            key= "asigned_work_id"
        )

    DataFileController.add_new_maintenance(new_maintenance.to_dict())
    return CreateMaintenanceCases.CORRECT

if __name__ == '__main__':
    print (create_maintenance_order(
        supervisor_id= 'f70b82d0-5a56-498b-ab3f-6d6fc488b99c',
        maintenance_date= date.today(),
        details= 'Un mantenimiento creado para hacer una prueba',
        asigned_technicians_id= ['14055690-f985-4e40-ac3e-4ec753438604'],
        name= 'arreglar carros',
        equipment_id= "19e68c4f-3f1f-4e4f-8ee3-22b7c3022a3e"
    ).value )