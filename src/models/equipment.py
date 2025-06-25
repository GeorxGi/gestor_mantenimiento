class Equipment:
    def __init__(self, *, code:str, name:str, description:str, provider:str):
        self.code:str = code
        self.name:str = name
        self.description:str = description
        self.provider:str = provider

    @classmethod
    def from_dict(cls, data:dict):
        return cls(
            code= data.get("code", ""),
            description= data.get("description", ""),
            name= data.get("name", ""),
            provider= data.get("provider", "")
        )