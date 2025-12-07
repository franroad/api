import jwt
from fastapi import HTTPException,status, Depends
from datetime import datetime,timezone,timedelta
from jwt.exceptions import InvalidTokenError,ExpiredSignatureError
from fastapi.security import OAuth2PasswordBearer
from . import database,models
from .config import settings
 
from  sqlalchemy.orm import Session


# in the "auth" endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth") #Looks for the token format: Authorization: Bearer <token>

# We will need secret key
#Algorithm we are gonna use 
#Expiration time 



def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire}) #Updating the varaibe, adding the expire time in the dict
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_access_token(user_token:str,credentials_exception):
    try:
        
        payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        id=payload.get("user_id") #Here we are geting the payload we have configured (the id)
        
        if id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "Not authenticated")
        
        #token_data=schemas.TokenData(id=id) in case validation is needed

    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Session Expired", headers={"WWW-Authenticate": "Bearer"})    
    except  InvalidTokenError:
        raise credentials_exception
   
    
    else:
    
        return id
    
def get_current_user(user_token: str= Depends(oauth2_scheme),db: Session = Depends(database.get_db)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Could not validte the Credentials", headers={"WWW-Authenticate": "Bearer"})
    user_id=verify_access_token(user_token,credentials_exception) # Returns decoded Token
    user=db.query(models.Users).filter(models.Users.id == user_id).first()
    
    return user
        
    
    