import os
from dotenv import load_dotenv
import bcrypt

load_dotenv()

_ENCRYPT_PASSWORD = os.getenv('ENCRYPT_PASSWORD') if os.getenv('ENCRYPT_PASSWORD') else ''

def hash_password(to_encript:str) -> str:
    salt = bcrypt.gensalt()

    hashed = bcrypt.hashpw(to_encript.encode(), salt)

    return hashed.decode('utf8')