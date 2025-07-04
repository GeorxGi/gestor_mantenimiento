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
        if not datestr or datestr == "None":
            return None
            
        # Lista de formatos de fecha a probar
        date_formats = [
            "%Y-%m-%d",      # 2024-12-15
            "%d-%m-%Y",      # 15-12-2024
            "%d/%m/%Y",      # 15/12/2024
            "%Y/%m/%d",      # 2024/12/15
            "%Y-%m-%d %H:%M:%S",  # 2024-12-15 10:30:00
            "%d-%m-%Y %H:%M:%S"   # 15-12-2024 10:30:00
        ]
        
        for fmt in date_formats:
            try:
                return datetime.strptime(str(datestr), fmt).date()
            except ValueError:
                continue
                
        # Si ningún formato funciona, intentar parsing automático
        try:
            from dateutil import parser
            return parser.parse(str(datestr)).date()
        except:
            return None

    @classmethod
    def from_dict(cls, data:dict):
        date_str = data.get("maintenance_date", "")
        if date_str:
            fecha_obj = datetime.strptime(date_str, "%d-%m-%Y").date()
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
