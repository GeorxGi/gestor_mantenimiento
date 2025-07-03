from src.controllers.sql.base_sql import BaseSqlController

class EquipmentSQL(BaseSqlController):
    def table(self):
        return "equipments"

    def create_equipment(self, *, code:str, name:str, description:str, provider:str) -> bool:
        """Metodo para ingresar una nueva fila en la columna de equipos"""
        if not code or not name or not description or not provider:
            return False
        return self._execute(
            query= f"""
            INSERT INTO {self.table()} (code, name, description, provider)
            VALUES (?, ?, ?, ?)
            """,
            params= (code, name, description, provider))

    def get_by_partial_name(self, name:str) -> list[dict]:
        """Metodo que retorna todas las instancias posibles en base a un nombre parcial"""
        if not name:
            return self.get_all_equipments()
        query= f"SELECT * FROM {self.table()} WHERE LOWER(name) LIKE ?"
        params = (f"%{name.lower()}%",)
        rows = self._fetchall(query= query, params= params)
        return [dict(row) for row in rows]
    
    def get_all_equipments(self) -> list[dict]:
        """Obtiene todos los equipos"""
        rows = self._fetchall(query=f"SELECT * FROM {self.table()}")
        return [dict(row) for row in rows]

    def delete_by_code(self, equipment_code:str) -> bool:
        """Elimina de la tabla el elemento con el id ingresado"""
        if not equipment_code:
            return False
        return self._execute(
            query= f"DELETE FROM {self.table()} WHERE code = ?",
            params= (equipment_code,)
        )

    def fetch_equipment_data(self, equipment_code:str) -> dict | None:
        data_fetch = self._fetchone(
            query=f"SELECT * FROM {self.table()} WHERE code = ?",
            params= (equipment_code,)
        )
        return dict(data_fetch) if data_fetch else None

if __name__ == '__main__':
    with EquipmentSQL() as db:
        value = db.get_by_partial_name("Lav")
        print(len(value))
        for item in value:
            print(item)