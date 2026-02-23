from fastapi import APIRouter, Depends,status,HTTPException,Response
from .. import schemas,database,models,utils
from .. import oauth
from  sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
router= APIRouter(
    #prefix="/auth",
    tags=['Authentication'] # This is mainly for improveing the readability of http://localhost:8000/docs
)

@router.post("/auth", response_model=schemas.Token)
def sign_in(user_cred:OAuth2PasswordRequestForm=Depends(),db: Session = Depends(database.get_db)):
    user = db.query(models.Users).filter(models.Users.email == user_cred.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Invalid credentials") #checks for the email
        
    if not utils.check(user_cred.password,user.password): # We are passing the user input and the aready stored passwod for compare hashing
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Invalid credentials") # checks the passwords match
    
    
    #Create token, we have used the user id as content of the token but can be any ohter field
    token=oauth.create_access_token(data={"user_id": user.id}) # we are passing the id in form of dictionary that is what is expecting
    #Return token
    return {"access_token": token, "token_type": "bearer","msg":"this message should not be displayed test pydantic"}
#Thanks to the pydantic response model we are only showing what we want.
