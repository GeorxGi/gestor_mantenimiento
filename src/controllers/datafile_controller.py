from pathlib import Path
import json
from src.enums.access_level import AccessLevel

class DataFileController:
    _BASE_DIR:Path = Path(__file__).parent.parent / "data"
    _BASE_DIR.mkdir(parents= True, exist_ok= True)

    REGISTERED_USERS:Path = _BASE_DIR / "registered_users.json"
    MAINTENANCES:Path = _BASE_DIR / "pending_maintenances.json"
    EQUIPMENTS:Path = _BASE_DIR / "equipments.json"

#--------------------------- LECTURA ARCHIVOS ---------------------------
    @staticmethod
    def __read_file(to_read_file:Path):
        try:
            with open(to_read_file, 'r') as file:
                data = json.load(file)
                yield from data
        except (json.JSONDecodeError, FileNotFoundError):
            return

    @staticmethod
    def read_users():
        """Metodo en el que se puede iterar para lectura de datos de usuarios"""
        yield from DataFileController.__read_file(DataFileController.REGISTERED_USERS)
    @staticmethod
    def read_users_by_access_level(access_level:AccessLevel):
        for usr in DataFileController.read_users():
            if AccessLevel.from_string(usr.get("access_level", "")) == access_level:
                yield usr

    @staticmethod
    def read_equipments():
        yield from DataFileController.__read_file(DataFileController.EQUIPMENTS)
    @staticmethod
    def read_maintenances():
        yield from DataFileController.__read_file(DataFileController.MAINTENANCES)

#--------------------------- ACTUALIZACIÓN ARCHIVOS ---------------------------

    @staticmethod
    def __update_file(*, to_read_file:Path, primary_key_name:str, primary_key_value, key_to_update: str, new_value, excluded_attributes:set[str]) -> bool:
        """Busca un registro por ID y modifica un único atributo."""
        try:
            with open(to_read_file, 'r') as file:
                data = json.load(file)

            file_updated = False
            for entry in data:
                if entry.get(primary_key_name) == primary_key_value:
                    if key_to_update in entry and key_to_update not in excluded_attributes:  # Restringe cambios en ID y contraseña
                        entry[key_to_update] = new_value
                        file_updated = True
                    break  # Modifica solo la primera coincidencia

            if file_updated:
                with open(to_read_file, 'w') as file:
                    json.dump(data, file, indent=4)  # Guarda los cambios
                return True
            return False

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error al actualizar archivo {to_read_file}: {e}")

        return False  # Si el usuario no fue encontrado o la clave no era válida

    @staticmethod
    def update_user(user_id:str, key:str, new_value) -> bool:
        return DataFileController.__update_file(
            to_read_file= DataFileController.REGISTERED_USERS,
            primary_key_name= "id",
            primary_key_value= user_id,
            key_to_update= key,
            new_value= new_value,
            excluded_attributes= {"id", "password", "access_level"}
        )

    @staticmethod
    def update_equipment(equipment_id:str, key:str, new_value) -> bool:
        return DataFileController.__update_file(
            to_read_file= DataFileController.EQUIPMENTS,
            primary_key_name= "id",
            primary_key_value= equipment_id,
            key_to_update= key,
            new_value= new_value,
            excluded_attributes= {"id"}
        )
#--------------------------- ADICIÓN ARCHIVOS ---------------------------

    @staticmethod
    def __add_to_file(file_path:Path, new_entry:dict) -> bool:
        try:
            if not file_path.exists(): #Si el archivo no existe, lo crea vacio rapidamente
                with open(file_path, 'w') as file:
                    json.dump([], file, indent= 4)

            with open(file_path, 'r+') as file:
                try: #Cargar datos del archivo json
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []

                data.append(new_entry)
                file.seek(0)
                json.dump(data, file, indent= 4)
                file.truncate()
                return True
        except (FileNotFoundError, IOError) as e:
            print(f"Error al añadir entrada en {file_path}: {e}")
            return False

    @staticmethod
    def add_new_user(new_user:dict) -> bool:
        return DataFileController.__add_to_file(
            DataFileController.REGISTERED_USERS,
            new_user
        )

    @staticmethod
    def add_new_equipment(new_equipment:dict) -> bool:
        return DataFileController.__add_to_file(
            DataFileController.EQUIPMENTS,
            new_equipment
        )

    @staticmethod
    def add_new_maintenance(new_maintenance:dict) -> bool:
        return DataFileController.__add_to_file(
            DataFileController.MAINTENANCES,
            new_maintenance
        )

#--------------------------- PRUEBAS UNITARIAS ---------------------------

if __name__ == '__main__':
    print (DataFileController.update_user(
        user_id="459f7897-b6f5-4309-a80b-75ec16c1c386",
        key= "fullname",
        new_value= "Jose Juan"
    ) )