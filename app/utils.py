from passlib.context import CryptContext
from . import schemas
pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pasword(password: str):
    hashed_password=pwd_context.hash(password)
    return hashed_password


def check(password: str,hashed_password:str): # the verify function returns a bool, is expecting 2 strings
    # input_password=pwd_context.hash(password)
    # stored_password=hashed_password
    return pwd_context.verify(password,hashed_password) # We have to use the verify function from passlib
      