from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import schemas,models,utils,database,oauth
from  sqlalchemy.orm import Session
from typing import Optional, List
from .. config import settings
from datetime import datetime,timezone,timedelta
router=APIRouter(
    prefix="/user",
    tags=['users']
)


@router.post("/add", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse) 
def create_user(new_user: schemas.Useradd, db: Session = Depends(database.get_db)):

    #hash the password - new_user.password
    #Updating the value for the password withthe return of the fucniton.
    new_user.password=utils.hash_pasword(new_user.password) #we are calling and sending the info to the funciton
    
    try: #prueba el codeigo
        user=models.Users(**new_user.dict())# This way we unpack the dictionary and put it in the same format the line above automatically
        db.add(user)
        db.commit()
        db.refresh(user)
    except:# si salta error haz esto
        raise HTTPException(status_code=422, detail="User already exists")
    else:  #si no hay error haz el return              
        
        return user


@router.get("/{id}",response_model=schemas.UserResponseGet) #resonse_model makes sure that unwanted field like password is not retrieved and shown
def get_user (id:int,db: Session = Depends(database.get_db),current_user:str =Depends(oauth.get_current_user)):
    print("RETURNED INFO:",current_user.email,current_user.id)
    user=db.query(models.Users).filter(models.Users.id == id).first()
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail=f"User with id: {id} not found")


@router.post("/recover_password")
def validate_user(current_user:schemas.UserSignin ,db: Session = Depends(database.get_db)):
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    print(current_user.email)
    user = db.query(models.Users).filter(models.Users.email == current_user.email).first()
    if user:
        code=utils.code_generator()
        hashed_code=utils.hash_pasword(code)
        thisdict = {"code": hashed_code,"email": current_user.email,"expires_at": expire}
        row=models.Code(**thisdict) # como ya es un diccionario no tiene el atributo.dict
        db.add(row)
        db.commit()
        print(hashed_code,thisdict)
        return {"info": "If user exists you will get an email"}
        
        
    
    else:
        return {"info": "user not found"}
    
