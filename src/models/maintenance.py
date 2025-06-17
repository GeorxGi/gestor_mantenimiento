class Maintenance:
    def __init__(self, maintenance_id:str, asigned_technicians_id:str):
        self.id:str = maintenance_id
        self.asigned_supervidor_id:str
        self.asigned_technicians_id:str = asigned_technicians_id
        self.is_pending:bool
        self.details:str