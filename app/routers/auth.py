from fastapi import APIRouter, Depends,status,HTTPException,Response
from .. import schemas,database,models,utils
from . import oauth
from  sqlalchemy.orm import Session
router= APIRouter(
    #prefix="/auth",
    tags=['Authentication'] # This is mainly for improveing the readability of http://localhost:8000/docs
)

@router.post("/auth")
def sign_in(user_cred:schemas.UserSignin,db: Session = Depends(database.get_db)):
    user = db.query(models.Users).filter(models.Users.email == user_cred.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Invalid credentials") #checks for the email
        
    if not utils.check(user_cred.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Invalid credentials (password)") # checks the passwords match
    
    
    #Create token, we have used the user id as content of the token but can be any ohter field
    token=oauth.create_access_token(data={"user_id": user.id}) # we are passing the id in form of dictionary that is what is expecting
    #Return token
    return token