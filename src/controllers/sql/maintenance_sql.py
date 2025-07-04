from src.controllers.sql.base_sql import BaseSqlController
from src.controllers.sql.equipment_sql import EquipmentSQL
from src.models.maintenance import Maintenance
from src.controllers.sql.user_sql import UserSQL

class MaintenanceSQL(BaseSqlController):
    def table(self):
        return "maintenance_orders"

    @staticmethod
    def second_table() -> str:
        return "maintenance_technicians"

    def create_maintenance_order(self, new_maintenance:Maintenance) -> bool:
        """Almacena la nueva orden de mantenimiento en la base de datos"""
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
        """Obtiene todos los mantenimientos pendientes de un supervisor"""
        rows = self._fetchall(
            query= f"SELECT * FROM {self.table()} WHERE supervisor_id = ? AND is_pending = TRUE",
            params= (supervisor_id, )
        )
        maintenances = []
        for row in rows:
            maintenance = Maintenance(
                maintenance_id=row[0],
                supervisor_id=row[1],
                equipment_code=row[2],
                maintenance_date=Maintenance.get_date_by_string(row[3]),
                is_pending=bool(row[4]),
                details=row[5],
                asigned_technicians_id=[]
            )
            maintenances.append(maintenance)
        return maintenances

    def fetchall_technicians_in_maintenance(self, maintenance_id:str) -> list[str]:
        """Obtiene el id de todos los técnicos asignados a un mantenimiento"""
        if not maintenance_id:
            return []
        value = self._fetchall(
            query= f"SELECT technician_id FROM {self.second_table()} WHERE maintenance_id = ?",
            params= (maintenance_id, )
        )
        return [row for row in value]

    def fetch_maintenance_basic_info(self, maintenance_id:str) -> dict:
        """Devuelve datos básicos sobre un mantenimiento como detalles, fecha y nombre del equipo)"""
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
        """Indica si el equipo ingresado posee un mantenimiento pendiente o no"""
        has_maintenance = self._fetchone(
            query= f"SELECT 1 FROM {self.table()} WHERE equipment_id = ?",
            params= (equipment_code,)
        )
        return True if has_maintenance else False

    def set_maintenance_no_longer_pending(self, maintenance_id:str) -> bool:
        """Establece el estado del mantenimiento a no pendiente y retorna un booleano que indica si
        la fila fue modificada exitosamente"""
        return self._execute(
            query= f"UPDATE {self.table()} SET is_pending = 0 WHERE id = ?",
            params= (maintenance_id, )
        )

    def fetchall_technician_maintenances(self, technician_id:str) -> list[dict]:
        """Obtiene una lista con el historial de todos los mantenimientos de un técnico con datos como
        nombre del supervisor que lo asigno, detalles, fecha de mantenimiento y estado (pendiente o completado)"""
        query= f"""
            SELECT
            u.fullname AS supervisor_name,
            m.details,
            m.maintenance_date,
            m.is_pending
            FROM {self.table()} m
            INNER JOIN {self.second_table()} mt ON mt.maintenance_id = m.id
            INNER JOIN {UserSQL().table()} u ON u.id = m.supervisor_id
            WHERE mt.technician_id = ?
            ORDER BY m.maintenance_date DESC
        """
        rows = self._fetchall(query= query, params= (technician_id, ))
        return [
            {
                "supervisor": row[0],
                "details": row[1],
                "date": row[2],
                "status": "Pendiente" if row[3] else "Completado"
            }
            for row in rows
        ]

    def fetchall_maintenance_orders(self) -> list[Maintenance]:
        """Obtiene todas las órdenes de mantenimiento"""
        rows = self._fetchall(
            query= f"SELECT * FROM {self.table()}",
            params= ()
        )
        maintenances = []
        for row in rows:
            maintenance = Maintenance(
                maintenance_id=row[0],
                supervisor_id=row[1],
                equipment_code=row[2],
                maintenance_date=Maintenance.get_date_by_string(row[3]),
                is_pending=bool(row[4]),
                details=row[5],
                asigned_technicians_id=[]
            )
            maintenances.append(maintenance)
        return maintenances

if __name__ == '__main__':
    with MaintenanceSQL() as db:
        print(db.fetchall_technicians_in_maintenance("5289faea-f996-46e6-9de5-034792128d4e"))