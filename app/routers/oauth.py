import jwt
from datetime import datetime,timezone,timedelta
from jwt.exceptions import InvalidTokenError

# We will need secret key
#Algorithm we are gonna use 
#Expiration time 

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta | None= timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    if expires_delta: #If expires delta is defined this is executed
        expire = datetime.now(timezone.utc) + expires_delta
    else:#default if timedelta is not defined
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt