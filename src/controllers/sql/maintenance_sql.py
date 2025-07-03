from src.controllers.sql.base_sql import BaseSqlController
from src.controllers.sql.equipment_sql import EquipmentSQL
from src.models.maintenance import Maintenance

class MaintenanceSQL(BaseSqlController):
    def table(self):
        return "maintenance_orders"

    @staticmethod
    def second_table() -> str:
        return "maintenance_technicians"

    def create_maintenance_order(self, new_maintenance:Maintenance) -> bool:
        """Almacena la nueva orden de mantenimiento en la database"""
        first_query = self._execute(
            query= f"INSERT INTO {self.table()} "
                   f"(id, supervisor_id, equipment_code, maintenance_date, is_pending, details) "
                   f"VALUES (?, ?, ?, ?, ?, ?)",
            params= (
                new_maintenance.id,
                new_maintenance.supervisor_id,
                new_maintenance.equipment_code,
                str(new_maintenance.maintenance_date),
                new_maintenance.is_pending,
                new_maintenance.details
            )
        )
        if not first_query:
            return False
        second_query = 0
        for technician_id in new_maintenance.asigned_technicians_id:
            second_query = second_query + self._execute(
                query= f"INSERT INTO {self.second_table()} (maintenance_id, technician_id) VALUES (?, ?)",
                params= (new_maintenance.id, technician_id)
            )
        if second_query != len(new_maintenance.asigned_technicians_id):
            return False
        return True

    def fetchall_supervisor_pending_maintenances(self, supervisor_id:str):
        return self._fetchall(
            query= f"SELECT * FROM {self.table()} WHERE supervisor_id = ? AND is_pending = TRUE",
            params= (supervisor_id, )
        )

    def fetchall_technicians_in_maintenance(self, maintenance_id:str) -> list[str]:
        if not maintenance_id:
            return []
        value = self._fetchall(
            query= f"SELECT technician_id FROM {self.second_table()} WHERE maintenance_id = ?",
            params= (maintenance_id, )
        )
        return [row for row in value]

    def fetch_maintenance_basic_info(self, maintenance_id:str) -> dict:
        query = f"""
            SELECT m.details, m.maintenance_date, e.name
            FROM {self.table()} m
            JOIN {EquipmentSQL().table()} e ON m.equipment_code = e.code
            WHERE m.id = ?
        """
        row = self._fetchone(query, params= (maintenance_id, ))
        if not row:
            return {}
        else:
            return{
                "details": row[0],
                "date": row[1],
                "equipment_name": row[2]
            }

    def equipment_has_pending_maintenance(self, equipment_code:str) -> bool:
        has_maintenance = self._fetchone(
            query= f"SELECT 1 FROM {self.table()} WHERE equipment_id = ?",
            params= (equipment_code,)
        )
        return True if has_maintenance else False

    def set_maintenance_no_longer_pending(self, maintenance_id:str) -> bool:
        """Establece el estado del mantenimiento a no pendiente y retorna un booleano que indica si
        la fila fue modificada exitosamente"""
        if not maintenance_id:
            return False
        return self._execute(
            query= f"UPDATE {self.table()} SET is_pending = 0 WHERE id = ?",
            params= (maintenance_id, )
        )

if __name__ == '__main__':
    with MaintenanceSQL() as db:
        print(db.fetchall_technicians_in_maintenance("5289faea-f996-46e6-9de5-034792128d4e"))