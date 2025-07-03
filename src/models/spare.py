class Spare:
    def __init__(self, *, code:int, name:str, amount:int, image_path:str):
        self.code:int = code
        self.name:str = name
        self.amount:int = amount
        self.image_path:str = image_path