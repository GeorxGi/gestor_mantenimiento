import io

from src.consts.file_dir import SPARE_IMAGES_PATH
import os

from src.controllers.sql.spare_sql import SpareSQL
from src.enums.create_spare_cases import CreateSpareCases
from PIL import Image

def process_and_store_image(image_bytes, output_path:str):
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
    #Valida que no se hayan ingresado datos en blanco
    if not name or not amount:
        return CreateSpareCases.EMPTY_INPUT
    #Valida que no se intenten almacenar cero piezas en la DB
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
        process_and_store_image(image_bytes, image_path)

    return CreateSpareCases.CORRECT

if __name__ == '__main__':
    test_image_path = "D:/Grabaciones/Marvel Rivals/Marvel Rivals_2024.12.06-01.20.png"

    with open(test_image_path, "rb") as file:
        img_byt = file.read()

    add_spare(
        name= 'Pieza de prueba',
        amount= 5,
        image_bytes= img_byt
    )
