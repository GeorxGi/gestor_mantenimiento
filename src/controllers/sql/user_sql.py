from src.controllers.sql.base_sql import BaseSqlController
from src.enums.access_level import AccessLevel

from uuid import uuid4

class UserSQL(BaseSqlController):
    def table(self):
        return "users"

    @property
    def public_fields(self):
        return "id, fullname, email, access_level, assigned_maintenance_id"

    def create_user(self,*, fullname:str, username:str, password:str, email:str, access_level:AccessLevel,):
        assigned_maintenance_id = None
        new_id = str(uuid4())

        self._execute(
            query= f"""
                INSERT INTO {self.table()} (id, fullname, username, password, email, access_level, assigned_maintenance_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
            params= (new_id, fullname, username, password, email, access_level.name, assigned_maintenance_id))

    def fetch_by_username(self, username:str) -> dict:
        row = self._fetchone(
            query= f"SELECT {self.public_fields} FROM {self.table()} WHERE username = ?",
            params= (username,)
        )
        return dict(row) if row else None

    def login_fetch(self, username:str) -> dict:
        row = self._fetchone(
            query= f"SELECT username, password FROM {self.table()} WHERE username = ?",
            params= (username, )
        )
        return dict(row) if row else None

    def fetch_by_access_level(self, access_level:AccessLevel) -> list[dict]:
        return [
            dict(row) for row in self._fetchall(
            query= f"SELECT {self.public_fields} FROM {self.table()} WHERE access_level = ?",
            params=(access_level.name,)
            )
        ]

    def fetch_user_by_id(self, user_id:str) -> dict:
        row = self._fetchone(
            query= f"SELECT {self.public_fields} FROM {self.table()} WHERE id = ?",
            params= (user_id, )
        )
        return dict(row)

    def fetchall_by_id(self, user_ids:list[str]) -> list[dict]:
        if not user_ids:
            return []
        placeholder = ", ".join("?" for _ in user_ids)

        rows = self._fetchall(
            query= f"SELECT {self.public_fields} FROM {self.table()} WHERE id IN ({placeholder})",
            params= tuple(user_ids)
        )
        return [dict(row) for row in rows]

    def fetch_not_busy_technicians(self) -> list[dict]:
        return[
            dict(row) for row in self._fetchall(
                query= f"""
                    SELECT {self.public_fields} FROM {self.table()}
                    WHERE access_level = ?
                    AND assigned_maintenance_id IS NULL
                    """,
                params= (AccessLevel.TECHNICIAN.name, )
            )
        ]

    def update_all_technicians_assigned_maintenance(self, maintenance_id: str | None, tech_id:list[str]):
        if not tech_id:
            return

        placeholder = ", ".join("?" for _ in tech_id)
        self._execute(
            query=f"""
                UPDATE {self.table()} SET assigned_maintenance_id = ?
                WHERE id IN ({placeholder})
                AND access_level = ?
                """,
            params= (maintenance_id, *tech_id, AccessLevel.TECHNICIAN.name)
        )

if __name__ == '__main__':
    with UserSQL() as db:
        response = db.fetch_not_busy_technicians()
        for value in response:
            print(value)