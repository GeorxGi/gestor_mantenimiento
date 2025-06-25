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

def create_maintenance_order(*, equipment_code:str, supervisor_id:str, asigned_technicians_id:list[str], name:str, details:str, maintenance_date:date) -> CreateMaintenanceCases:
    #Verifica que los datos de entrada no estén vacios
    if not equipment_code or not supervisor_id or not asigned_technicians_id or not name or not details or not maintenance_date:
        return CreateMaintenanceCases.EMPTY_IMPUT

    # Verifica que el id del equipo ingresado exista
    if not equipment_exists(equipment_code):
        return CreateMaintenanceCases.EQUIPMENT_NOT_FOUND

    with UserSQL() as db:
        in_db_technicians = db.fetchall_by_id(asigned_technicians_id)

        if len(in_db_technicians) != len(asigned_technicians_id):
            return CreateMaintenanceCases.NOT_REGISTERED_ID

        for technician in in_db_technicians:
            technician_access_level = AccessLevel.from_string(technician.get("access_level", ""))
            if technician_access_level != AccessLevel.TECHNICIAN:
                return CreateMaintenanceCases.TECHNICIAN_ID_IS_NOT_TECHNICIAN

        supervisor_row = db.fetchone_by_id(supervisor_id)
        super_access_level = AccessLevel.from_string(supervisor_row.get("access_level", ""))
        if super_access_level != AccessLevel.SUPERVISOR:
            return CreateMaintenanceCases.SUPERVISOR_ID_IS_NOT_SUPERVISOR

    if maintenance_date < date.today():
        return CreateMaintenanceCases.NOT_VALID_DATE

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
        for tech in asigned_technicians_id:
            db.update_assigned_work_id(
                work_id= new_maintenance.id,
                tech_id= tech,
            )
    with MaintenanceSQL() as db:
        db.create_maintenance_order(
            new_maintenance= new_maintenance,
        )
    return CreateMaintenanceCases.CORRECT

def get_supervisor_pending_maintenances(supervisor_id:str) -> list[Maintenance]:
    """Obtiene una lista con todos los mantenimientos pendientes asignados por un supervisor"""
    if not supervisor_id:
        return []
    with MaintenanceSQL() as db:
        pending_maintenances = db.fetchall_supervisor_pending_maintenances(supervisor_id)
        return pending_maintenances

if __name__ == '__main__':
    print (create_maintenance_order(
        supervisor_id= "ae6593c2-37fc-4370-9842-e97fda494faf",
        maintenance_date= date.today(),
        details= "Mantenimiento de prueba",
        name= "Arreglar lavadora",
        asigned_technicians_id= ["732bd507-9223-4fa2-bc7a-598026352f22"],
        equipment_code= "a16ebe3c-3efe-43ac-817a-15a83ef54e04"
    ).value)

    #for item in get_supervisor_pending_maintenances("f70b82d0-5a56-498b-ab3f-6d6fc488b99c"):
    #    print (item.to_dict())