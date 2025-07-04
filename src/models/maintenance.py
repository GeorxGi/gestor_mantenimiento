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

    @staticmethod
    def get_date_by_string(datestr:str) -> date | None:
        try:
            date_obj = datetime.strptime(datestr, "%d-%m-%Y").date()
            if not date_obj:
                date_obj = datetime.strptime(datestr, "%Y-%m-%d").date()
            return date_obj
        except Exception:
            return None

    @classmethod
    def from_dict(cls, data:dict):
        date_str = data.get("maintenance_date", "")
        fecha_obj = Maintenance.get_date_by_string(date_str)

        return cls(
            maintenance_id= data.get("id", ""),
            supervisor_id= data.get("supervisor_id", ""),
            asigned_technicians_id= data.get("asigned_technicians_id", []),
            equipment_code= data.get("equipment_id", ""),
            is_pending= bool(data.get("is_pending", "")),
            maintenance_date= fecha_obj,
            details= data.get("details", "")
        )
