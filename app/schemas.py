from pydantic import BaseModel, field_serializer, computed_field, EmailStr,Field,ConfigDict,NonNegativeInt,conint
from datetime import datetime
from typing import Dict, Any



    
    
    



class Post (BaseModel): # here we use pydantic for define the schema
    title: str
    content: str
    published: bool = True # this is an optional/odefault to true
   


class PostUpdate (Post): # here we use our Post model to defina the schema
    pass #we are getting the values from the Post


     
class OpResponse (BaseModel):
    email:str
    created_at:datetime= Field(serialization_alias='Joined')
    
    @field_serializer("created_at")
    def format_created_at(self, dt: datetime, _) -> str:
        return dt.strftime("%Y-%m-%d %H:%M")
    
    
class PostResponse (BaseModel): #This model defines the response that the user will get
     title: str
     content: str
     id: int
     created_at: datetime
     user_id: int
     op:OpResponse
     


     @field_serializer("created_at")
     def format_created_at(self, dt: datetime, _) -> str:
        return dt.strftime("%Y-%m-%d %H:%M")

    
    # op: OpResponse # De esta forma lo tenemos nested si no serie op_email,op_created_at
    


class PostVotes(BaseModel):
    PostORM:PostResponse=Field(serialization_alias='Post🪆')
    Likes:int=Field(serialization_alias='Likes💯')
    



class PostResponseUpdate (PostResponse): #This model defines the response that the user will get
    pass
    @computed_field # This is for sending  a message
    @property
    def message(self) -> str:
        # now you can refer to self.email
        return "Post updated Succesfully"
    
########################################USERS#########################################################
#USERS
########################################USERS#########################################################

class Useradd(BaseModel):
    email:EmailStr
    password:str


class UserResponse (BaseModel):
    email:str
    created_at: datetime

    @field_serializer("created_at")
    def format_created_at(self, dt: datetime, _) -> str:
        return dt.strftime("%Y-%m-%d %H:%M")
    

    @computed_field # This is for sending  a message
    @property
    def message(self) -> str:
        # now you can refer to self.email
        return f"User {self.email!r} created successfully" # !r is for obtaining the mail between quotes
   
class UserResponseGet (BaseModel): #Configurado para que no muestre la password
    id: int
    email:str
    created_at: datetime

    @field_serializer("created_at")
    def format_created_at(self, dt: datetime, _) -> str:
        return dt.strftime("%Y-%m-%d %H:%M")

class UserSignin(BaseModel):
    email:EmailStr

# class UserPost(BaseModel):
#     op:str

########################################TOKEN#########################################################
#TOKEN
########################################TOKEN#########################################################

class Token(BaseModel):
    access_token:str
    token_type:str


########################################E-mail#########################################################
#E-mail
########################################E-mail#########################################################
class EmailMessage(BaseModel):
    subject:str
    recipients:list[EmailStr]
    body:str
    
########################################update-password#########################################################
#Update Password
########################################update-password#########################################################
class UpdatePassword(BaseModel):
    email:EmailStr
    code:int
    new_password:str

########################################Vote#########################################################
#Vote
########################################Vote#########################################################

class Vote(BaseModel):
    post_id:NonNegativeInt # No permite numeros negativos
    like:int= Field(ge=0,le=1)#Permite establecer un rango