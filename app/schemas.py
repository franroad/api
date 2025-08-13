from pydantic import BaseModel, field_serializer, ConfigDict
from datetime import datetime

class Post (BaseModel): # here we use pydantic for define the schema
    title: str
    content: str
    published: bool = True # this is an optional/odefault to true


class PostUpdate (Post): # here we use our Post model to defina the schema
    pass #we are getting the values from the Post

class PostResponse (BaseModel): #This model defines the response that the user will get
    title: str
    content: str
    id: int
    created_at: datetime
    
    # @field_serializer("created_at")
    # def format_created_at(self, dt: datetime, _) -> str:
    #     return dt.strftime("%Y-%m-%d %H:%M")
    
   

   
