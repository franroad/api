from fastapi import APIRouter, Depends,status,HTTPException,Response
from .. import schemas,database,models
from  sqlalchemy.orm import Session
router= APIRouter(
    #prefix="/auth",
    tags=['Authentication'] # This is mainly for improveing the readability of http://localhost:8000/docs
)

@router.post("/auth")
def sign_in(user_cred:schemas.UserSignin,db: Session = Depends(database.get_db)):
    user = db.query(models.Users).filter(models.Users.email == user_cred.email).first()

    if user:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "User not found")