
```python
 from fastapi import FastAPI #import the library
 from fastapi.params import Body

 app=FastAPI() #create instance of fastapi

 @app.get("/fran")#the route where to find the stuff /fran would be: http://127.0.0.1:8000/fran (decorator , endpoint)
 def root(): #root=funtion name (does not matter)
     return {"message": "Hello World"}

 @app.get("/posts")
 def get_posts():
     return{"data": "this is your posts"}

 @app.post("/createpost")
 def create_posts(payload: dict =Body(...)): #this gets the body from the post ,convert into a python dictionary and print save it into variable
     print (payload)
     return{"new_post": f"title: {payload['title']}"+" , succesfully created post"}


```

# Using Pydantic

```python
from typing import Optional
from fastapi import FastAPI #import the library
from fastapi.params import Body
from pydantic import BaseModel

app=FastAPI() #create instance of fastapi

class Post (BaseModel): # here we use pydantic for define the schema
    title: str
    content: str
    published: bool = True # this is an optional/odefault to true
    rating: Optional[int]= None #Optional filed with no default value , type integer
    
    

@app.get("/fran")#the route where to find the stuff /fran would be: http://127.0.0.1:8000/fran (decorator , endpoint)
def root(): #root=funtion name (does not matter)
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return{"data": "this is your posts"}

@app.post("/createpost")
def create_posts(new_post: Post): #We are refenrcing the Post class that validates if the post meets the scheme requirements(pydantic)
    print (new_post)# print is internal, we are not retunring info to the client.
    print (new_post.dict()) #Converting  the Pydantic model into a dict
    return{"message_from_server": "new post added, " f"title: {new_post.title}"} # accessing the title attribute of  new_poost

#title str, content str, category

```