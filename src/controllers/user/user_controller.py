#
# LOGICA CON EL MANEJO DE USUARIOS
# * verificar nivel de acceso, entre otro
#

from src.enums.access_level import AccessLevel
from src.models.users.admin import Admin
from src.models.users.technician import Technician
from src.models.users.supervisor import Supervisor
from src.models.users.user import User

def check_access_level(user:User):
    return user.get_access_level()