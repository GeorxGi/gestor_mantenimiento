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

    def delete_spare(self, spare_code:int) -> bool:
        if not spare_code:
            return False
        return self._execute(
            query= f"DELETE FROM {self.table()} WHERE code = ?",
            params= (spare_code, )
        )

    def fetch_by_code(self, spare_code:int) -> dict:
        """Obtiene un spare en base al codigo ingresado"""
        return dict(
            self._fetchone(
                query= f"SELECT * FROM {self.table()} WHERE code = ?",
                params= (spare_code, )
            )
        )
    def discount_spare_stock(self, code:int, amount:int, ):
        self._execute(
            query= f"""
                UPDATE {self.table()}
                SET amount = amount - ?
                WHERE code = ? 
            """,
            params= (amount, code)
        )

    def add_spare_stock(self, code:int, amount:int):
        self._execute(
            query= f"""
                UPDATE {self.table()}
                SET amount = amount + ?
                WHERE code = ? 
            """,
            params= (amount, code)
        )

if __name__ == '__main__':
    with SpareSQL() as db:
        print(db.fetch_all_spares())