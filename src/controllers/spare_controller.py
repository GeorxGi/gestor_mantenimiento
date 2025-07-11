import io

from src.consts.file_dir import SPARE_IMAGES_PATH
import os

from src.models.spare import Spare
from src.controllers.sql.spare_sql import SpareSQL

from src.enums.create_spare_cases import CreateSpareCases

from PIL import Image

def __process_and_store_image(image_bytes, output_path:str):
    #Valída que los bytes ingresados representen una imagen
    try:
        with Image.open(io.BytesIO(image_bytes)) as img:
            img.verify()


        #Comprime y retorna la imagen ingresada
        max_img_width = 500
        with Image.open(io.BytesIO(image_bytes)) as img:
            img = img.convert("RGB")

            #Redimensiona la imágen (en caso de ser muy grande)
            if img.width > max_img_width:
                ratio = max_img_width / img.width
                new_size = (max_img_width, int(img.height * ratio))
                img = img.resize(new_size, Image.Resampling.LANCZOS)

            #Almacenar la imágen
            os.makedirs(SPARE_IMAGES_PATH, exist_ok= True)
            img.save(output_path, format= "JPEG", quality= 80, optimize= True)
            return True
    except Exception as e:
        print(e)
        return False

def add_spare(name:str, amount:int, image_bytes:bytes=None) -> CreateSpareCases:
    #Valída que no se hayan ingresado datos en blanco
    if not name or not amount:
        return CreateSpareCases.EMPTY_INPUT
    #Valída que no se intenten almacenar cero piezas en la DB
    if amount <= 0:
        return CreateSpareCases.INVALID_AMOUNT

    #Crea la pieza en la DB y obtiene el código que se le fue asignado (autoincremental)
    with SpareSQL() as db:
        spare_code = db.create_part(name= name, amount= amount)

    #Si no se retorna el código de la pieza, se retorna un error inesperado
    if not spare_code:
        return CreateSpareCases.UNKNOWN_ERROR

    #Almacena la imagen en el directorio data
    if image_bytes:
        os.makedirs(SPARE_IMAGES_PATH, exist_ok= True)
        image_path = f"{SPARE_IMAGES_PATH}/{spare_code}.jpg"
        __process_and_store_image(image_bytes, image_path)

    return CreateSpareCases.CORRECT

def get_spare_by_partial_name(partial_str:str) -> list[Spare]:
    with SpareSQL() as db:
        data = db.fetch_all_spares() if not partial_str else db.fetch_by_partial_name(partial_str)
        return [Spare.from_dict(spr) for spr in data]

def remove_spare_from_inventory(spare_code:int) -> bool:
    if not spare_code:
        return False
    with SpareSQL() as db:
        return db.delete_spare(spare_code)

def discount_spare_stock(spare_code:int, request_ammount:int) -> bool:
    """Metodo para sustraer repuestos de la base de datos (retorna falso si no se encontro o no hay suficiente cantidad)"""
    if not spare_code or not request_ammount:
        return False
    with SpareSQL() as db:
        result = db.fetch_by_code(spare_code)
        spare = Spare.from_dict(result)
        if spare.amount < request_ammount:
            return False
        db.discount_spare_stock(amount= request_ammount, code= spare.code)
        return True

def add_spare_stock(spare_code:int, to_add_amount:int) -> bool:
    """Metodo para reponer inventario de una pieza determinada"""
    if not spare_code or not to_add_amount:
        return False
    with SpareSQL() as db:
        db.add_spare_stock(spare_code, to_add_amount)
        return True

if __name__ == '__main__':
    get_spare_by_partial_name("")
