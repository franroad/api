from passlib.context import CryptContext
from . import schemas
pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pasword(password):
    hashed_password=pwd_context.hash(password)
    return hashed_password
