from src.controllers.sql.base_sql import BaseSqlController

class SpareSQL(BaseSqlController):
    def table(self) -> str:
        return 'spare_inventory'

    def create_part(self, name:str, amount:int) -> int:
        cursor = self.connection.execute(
            f"INSERT INTO {self.table()} (name, amount) VALUES (?, ?)",
            (name, amount)
        )
        self.connection.commit()
        return cursor.lastrowid #Retorna el codigo de pieza generado

    def fetch_all_spares(self) -> list[dict]:
        data = self._fetchall(query= f"SELECT * FROM {self.table()}", params= ())
        return [dict(value) for value in data]

    def fetch_by_partial_name(self, part_str:str) -> list[dict]:
        if not part_str:
            return self.fetch_all_spares()

        data = self._fetchall(
            query= f"SELECT * FROM {self.table()} WHERE LOWER(name) LIKE ?",
            params= (f"%{part_str.lower()}%",)
        )
        return [dict(value) for value in data]

if __name__ == '__main__':
    with SpareSQL() as db:
        print(db.fetch_all_spares())