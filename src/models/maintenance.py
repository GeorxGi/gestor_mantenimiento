from datetime import date, datetime

class Maintenance:
    def __init__(self, *, equipment_code:str, supervisor_id:str, maintenance_id:str, asigned_technicians_id:list[str], is_pending:bool, details:str, maintenance_date:date):
        self.id:str = maintenance_id
        self.supervisor_id:str = supervisor_id
        self.asigned_technicians_id:list[str] = asigned_technicians_id
        self.equipment_code:str = equipment_code
        self.is_pending:bool = is_pending
        self.details:str = details
        self.maintenance_date:date = maintenance_date

    def to_dict(self) -> dict:
        data = {key: value for key, value in vars(self).items() if key != "maintenance_date"}
        data["maintenance_date"] = str(self.maintenance_date)
        return data

    @classmethod
    def from_dict(cls, data:dict):
        date_str = data.get("maintenance_date", "")
        if date_str:
            fecha_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        else:
            return None

        return cls(
            maintenance_id= data.get("id", ""),
            supervisor_id= data.get("supervisor_id", ""),
            asigned_technicians_id= data.get("asigned_technicians_id", []),
            equipment_code= data.get("equipment_id", ""),
            is_pending= bool(data.get("is_pending", "")),
            maintenance_date= fecha_obj,
            details= data.get("details", "")
        )
