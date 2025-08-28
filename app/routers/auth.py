from fastapi import APIRouter, Depends,status,HTTPException,Response
from .. import schemas,database,models,utils
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

    #Create token
    #Return token
    return user