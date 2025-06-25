import sqlite3
from pathlib import Path
from abc import ABC, abstractmethod

class BaseSqlController(ABC):
    _DB_PATH = Path(__file__).parent.parent.parent / "data" / "local_storage.db"
    _SCHEMA_PATH = Path(__file__).parent / "schema.sql"

    def __init__(self):
        self.connection = sqlite3.connect(self._DB_PATH)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _execute(self, query:str, params:tuple = ()) -> bool:
        """Metodo para ejecutar un query SQL, retorna un booleano que indica si alguna fila fue modificada"""
        self.cursor.execute(query, params)
        self.connection.commit()
        return self.cursor.rowcount > 0

    def _fetchone(self, query:str, params:tuple = ()):
        """Metodo para obtener una única instancia de datos de la tabla"""
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def _fetchall(self, query:str, params:tuple = ()):
        """Metodo para obtener todas las instancias de datos de la tabla"""
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        """Cerrar la conexión con la base de datos"""
        self.connection.close()

    @staticmethod
    def init_db():
        if not BaseSqlController._SCHEMA_PATH.exists():
            raise FileNotFoundError("Archivo schema.sql no encontrado")
        with sqlite3.connect(BaseSqlController._DB_PATH) as conn:
            with open(BaseSqlController._SCHEMA_PATH, "r", encoding="utf-8") as f:
                conn.executescript(f.read())

    @abstractmethod
    def table(self) -> str:
        """Metodo obligatorio para definir nombre o estructura de la tabla"""
    pass