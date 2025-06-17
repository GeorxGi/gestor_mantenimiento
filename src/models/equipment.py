from datetime import date

class Equipment:
    def __init__(self):
        self.code:str
        self.name:str
        self.description:str
        self.provider:str
        self.maintenance_date:date