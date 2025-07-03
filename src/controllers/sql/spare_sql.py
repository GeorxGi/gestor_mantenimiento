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