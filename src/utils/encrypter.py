import os
from dotenv import load_dotenv
import bcrypt

load_dotenv()

_ENCRYPT_PASSWORD = os.getenv('ENCRYPT_PASSWORD') if os.getenv('ENCRYPT_PASSWORD') else ''
_ENCODE_TYPE = 'utf-8'

def hash_password(to_encript:str) -> str:
    hashed = bcrypt.hashpw(to_encript.encode(_ENCODE_TYPE), bcrypt.gensalt())

    return hashed.decode(_ENCODE_TYPE)

def compare_hashed(password_plaintext:str, hashed:str):
    return bcrypt.checkpw(
        password_plaintext.encode(_ENCODE_TYPE),
        hashed.encode(_ENCODE_TYPE)
    )