from fastapi import status, HTTPException, Depends, APIRouter,BackgroundTasks
from .. import schemas,models,utils,database,oauth,mail
from  sqlalchemy.orm import Session

from .. config import settings
from datetime import datetime,timezone,timedelta
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from  sqlalchemy import desc


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
def validate_user(background_tasks: BackgroundTasks, current_user:schemas.UserSignin ,db: Session = Depends(database.get_db)):
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
        #mail.send_email(code)
        background_tasks.add_task(mail.send_email, code, user=current_user.email) #We use background task as send_mail is async funciton
        
        # Schedule send_email(code) to run in the background 
        # after the response is sent, without blocking the endpoint
        return {"info": "If user exists you will get an email"}
        
        
    
    else:
        return {"info": "user not found"}
    
@router.post("/update_password")
def validate_code(user_info:schemas.UpdatePassword,db: Session = Depends(database.get_db)):
    user = db.query(models.Users).filter(models.Users.email == user_info.email).first()
    try:
        db.query(models.Code).filter(models.Code.email == user_info.email).order_by(desc(models.Code.id)).limit(1).one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "request new code and retry in a couple of minuts")
    
    user_code=db.query(models.Code).filter(models.Code.email == user_info.email).order_by(desc(models.Code.id)).limit(1).one()
    
    print(user_code.id)
    input=str(user_info.code)
    existent=str(user_code.code)
    code_exp=user_code.expires_at
    print(code_exp)

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Invalid credentials") #checks for the email
        
    if not utils.check(input,existent): # We are passing the user input and the aready stored passwod for compare hashing
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Invalid Code")
   
    if datetime.now(timezone.utc)>=code_exp:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Code expired")

    else:
        return("input your password")
    
