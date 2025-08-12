from pydantic import BaseModel

class Post (BaseModel): # here we use pydantic for define the schema
    title: str
    content: str
    published: bool = True # this is an optional/odefault to true


class PostUpdate (Post): # here we use our Post model to defina the schema
    pass #we are getting the values from the Post