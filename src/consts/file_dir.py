from pathlib import Path

GLOBAL_DATA_PATH = Path(__file__).parent.parent / "data"

DB_SCHEMA_PATH = Path(__file__).parent.parent / "controllers" / "sql" / "schema.sql"

DB_PATH = GLOBAL_DATA_PATH / "local_storage.db"
SPARE_IMAGES_PATH = GLOBAL_DATA_PATH / "images" / "spares"


if __name__ == '__main__':
    print("Mostrando rutas DEBUG\n")

    print(GLOBAL_DATA_PATH)
    print(DB_SCHEMA_PATH)
    print(DB_PATH)
    print(SPARE_IMAGES_PATH)
