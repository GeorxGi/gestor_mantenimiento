#
# CONTROLADOR ENCARGADO DEL MANEJO DE MANTENIMIENTOS
# (Creación, modificación, etc)
#

from datetime import date
import uuid

from src.controllers.sql.user_sql import UserSQL
from src.enums.access_level import AccessLevel
from src.enums.create_maintenance_cases import CreateMaintenanceCases

from src.controllers.equipment_controller import equipment_exists

from src.controllers.sql.maintenance_sql import MaintenanceSQL

from src.models.maintenance import Maintenance

def create_maintenance_order(*, equipment_code:str, supervisor_id:str, asigned_technicians_id:list[str], details:str, maintenance_date:date) -> CreateMaintenanceCases:
    #Verifica que los datos de entrada no estén vacios
    if not equipment_code or not supervisor_id or not asigned_technicians_id or not details or not maintenance_date:
        return CreateMaintenanceCases.EMPTY_IMPUT

    # Verifica que el id del equipo ingresado exista
    if not equipment_exists(equipment_code):
        return CreateMaintenanceCases.EQUIPMENT_NOT_FOUND

    with UserSQL() as db:
        in_db_technicians = db.fetchall_by_id(asigned_technicians_id)
        supervisor_row = db.fetch_user_by_id(supervisor_id)

    #Verifica que los tecnicos ingresados no tengan un mantenimiento asignado
    for technician in in_db_technicians:
        value = technician.get("assigned_maintenance_id", "")
        if value is not None:
            return CreateMaintenanceCases.BUSY_TECHNICIAN

        #Verifica que los tecnicos ingresados si cumplan con ese rol (no sean supervisor por ejemplo)
        technician_access_level = AccessLevel.from_string(technician.get("access_level", ""))
        if technician_access_level != AccessLevel.TECHNICIAN:
            return CreateMaintenanceCases.TECHNICIAN_ID_IS_NOT_TECHNICIAN

    #Verifica que se haya encontrado a todos los técnicos en la DB
    if len(in_db_technicians) != len(asigned_technicians_id):
        return CreateMaintenanceCases.NOT_REGISTERED_ID

    #Verifica que el supervisor ingresado si cumpla con ese rol (no sea tecnico por ejemplo)
    super_access_level = AccessLevel.from_string(supervisor_row.get("access_level", ""))
    if super_access_level != AccessLevel.SUPERVISOR:
        return CreateMaintenanceCases.SUPERVISOR_ID_IS_NOT_SUPERVISOR

    #Verifica que la fecha de mantenimiento no sea menor a la fecha de hoy
    if maintenance_date < date.today():
        return CreateMaintenanceCases.NOT_VALID_DATE

    #A partir de aquí es almacenar en la base de datos
    new_maintenance = Maintenance(
        supervisor_id= supervisor_id,
        maintenance_id= str(uuid.uuid4()),
        asigned_technicians_id=asigned_technicians_id,
        maintenance_date= maintenance_date,
        details= details,
        is_pending= True,
        equipment_code= equipment_code
    )

    with UserSQL() as db:
        db.update_all_technicians_assigned_maintenance(
            maintenance_id= new_maintenance.id,
            tech_id= asigned_technicians_id,
        )

    with MaintenanceSQL() as db:
        db.create_maintenance_order(
            new_maintenance= new_maintenance,
        )
    return CreateMaintenanceCases.CORRECT

def conclude_maintenance(maintenance_id:str) -> bool:
    if not maintenance_id:
        return False
    with MaintenanceSQL() as db:
        technicians:list[str] = db.fetchall_technicians_in_maintenance(maintenance_id)
        db.set_maintenance_no_longer_pending(maintenance_id)

    with UserSQL() as db:
        db.update_all_technicians_assigned_maintenance(
            tech_id= technicians,
            maintenance_id= None
        )

    return True

def get_supervisor_pending_maintenances(supervisor_id:str) -> list[Maintenance]:
    """Obtiene una lista con todos los mantenimientos pendientes asignados por un supervisor"""
    if not supervisor_id:
        return []
    with MaintenanceSQL() as db:
        pending_maintenances = db.fetchall_supervisor_pending_maintenances(supervisor_id)
        return pending_maintenances

def get_maintenance_basic_info(maintenance_id:str) -> dict | None:
    """Retorna un diccionario con los campos description, date y equipment_name en caso de haber encontrado el mantenimiento"""
    if not maintenance_id:
        return None
    with MaintenanceSQL() as db:
        return db.fetch_maintenance_basic_info(maintenance_id)

def get_all_technician_maintenances(technician_id:str):
    if not technician_id:
        return None

    with MaintenanceSQL() as db:
        return db.fetchall_technician_maintenances(technician_id)

def get_equipment_maintenance_info(equipment_code:str) -> list[dict]:
    if not equipment_code:
        return []
    with MaintenanceSQL() as db:
        maint = db.fetchall_equipment_maintenances(equipment_code)
        return []
        #TERMINAR AQUI
        #return [Maintenance.from_dict(data) for data in maint]

if __name__ == '__main__':
    print(get_equipment_maintenance_info("TUPAPA"))
    print (get_all_technician_maintenances("f912486a-ff6e-4dca-bc66-101e87203a48"))