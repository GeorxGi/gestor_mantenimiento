class Equipment:
    def __init__(self, *, id:str, name:str, description:str, provider:str, maintenance_id:str):
        self.id:str = id
        self.name:str = name
        self.description:str = description
        self.provider:str = provider
        self.maintenance_id:str = maintenance_id