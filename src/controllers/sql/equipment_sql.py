from src.controllers.sql.base_sql import BaseSqlController

class EquipmentSQL(BaseSqlController):
    def table(self):
        return "equipments"

    def create_equipment(self, *, code:str, name:str, description:str, provider:str) -> bool:
        """Metodo para ingresar una nueva fila en la columna de equipos"""
        return self._execute(
            query= f"""
            INSERT INTO {self.table()} (code, name, description, provider)
            VALUES (?, ?, ?, ?)
            """,
            params= (code, name, description, provider))

    def get_by_partial_name(self, name:str) -> list[dict]:
        """Metodo que retorna todas las instancias posibles en base a un nombre parcial"""
        query= f"SELECT * FROM {self.table()} WHERE LOWER(name) LIKE ?"
        params = (f"%{name.lower()}%",)
        rows = self._fetchall(query= query, params= params)
        return [dict(row) for row in rows]

    def delete_by_id(self, equipment_id:str) -> bool:
        """Elimina de la tabla el elemento con el id ingresado"""
        return self._execute(
            query= f"DELETE FROM {self.table()} WHERE code = ?",
            params= (equipment_id, )
        )

    def fetch_equipment_data(self, equipment_id:str) -> dict | None:
        data_fetch = self._fetchone(
            query=f"SELECT * FROM {self.table()} WHERE code = ?",
            params= (equipment_id, )
        )
        return dict(data_fetch) if data_fetch else None

if __name__ == '__main__':
    with EquipmentSQL() as db:
        value = db.get_by_partial_name("Lav")
        print(len(value))
        for item in value:
            print(item)