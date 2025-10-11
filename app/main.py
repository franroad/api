

from fastapi import FastAPI #import the library
#for using stuff for the ORM definedo in app folder
from .database import engine
from . import models
from . routers import users,posts,auth,vote #points to the files whre are the api endpoints


models.Base.metadata.create_all(bind=engine)

app=FastAPI() #create instance of fastapi

app.include_router(posts.router) #Includes the routes defined in the files from the import and registers in the main.py
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)



@app.get("/")#the route where to find the stuff /fran would be: http://127.0.0.1:8000/fran (decorator , endpoint)
def root(): #root=funtion name (does not matter)
    return {"message": "Hello World 😬"}
