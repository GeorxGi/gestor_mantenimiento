from datetime import date

class Maintenance:
    def __init__(self, *, equipment_id:str, supervisor_id:str, maintenance_id:str, asigned_technicians_id:list[str], is_pending:bool, details:str, maintenance_date:date):
        self.id:str = maintenance_id
        self.supervisor_id:str = supervisor_id
        self.asigned_technicians_id:list[str] = asigned_technicians_id
        self.equipment_id:str = equipment_id
        self.is_pending:bool = is_pending
        self.details:str = details
        self.maintenance_date:date = maintenance_date


    def to_dict(self) -> dict:
        data = {key: value for key, value in vars(self).items() if key != "maintenance_date"}
        data["maintenance_date"] = str(self.maintenance_date)
        return data