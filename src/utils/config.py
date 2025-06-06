#
# ARCHIVO PARA CONFIGURACIONES DEL PROYECTO
# DIRECTORIOS,
#
from pathlib import Path
import os

_BASE_DIR = Path(__file__).parent.parent

REGISTERED_USERS_PATH = _BASE_DIR / "data" / "registered_users.json"

os.makedirs(_BASE_DIR / "data", exist_ok=True)