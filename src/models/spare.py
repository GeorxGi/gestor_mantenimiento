import os.path
from src.consts.file_dir import SPARE_IMAGES_PATH

class Spare:
    def __init__(self, *, code:int, name:str, amount:int, image_path:str = None):
        self.code:int = code
        self.name:str = name
        self.amount:int = amount
        self.image_path:str | None = image_path

    @classmethod
    def from_dict(cls, data:dict):
        code = int(data.get("code", ""))
        temp_path = f"{SPARE_IMAGES_PATH}/{code}.jpg"
        image_path = temp_path if os.path.exists(temp_path) else None

        return cls(
            code= int(data.get("code", "")),
            name= data.get("name", ""),
            amount= int(data.get("amount", "")),
            image_path= image_path
        )