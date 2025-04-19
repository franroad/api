
######
#using Pydantic
######

from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends #import the library
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange #importing the random for generating th post id
import psycopg2
from psycopg2.extras import RealDictCursor
import time
#for using stuff for the ORM definedo in app folder
from . import models
from .database import engine , get_db
from  sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

app=FastAPI() #create instance of fastapi



class Post (BaseModel): # here we use pydantic for define the schema
    title: str
    content: str
    published: bool = True # this is an optional/odefault to true


#Connecting to the DB 

#while True:
for i in range(5):

    try:
        conn = psycopg2.connect(host='localhost',database='api',user='api',password='1231', cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Succesful connection to DB") 
        break
    except Exception as error: #Exception, Python class to catch the errors.
        print("Connection to DB Failed")
        print("Error:", error)
        time.sleep(3)
else:
    print("All attempts to connect to the DB have failed")
    


@app.get("/")#the route where to find the stuff /fran would be: http://127.0.0.1:8000/fran (decorator , endpoint)
def root(): #root=funtion name (does not matter)
    return {"message": "Hello World"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)): #thanks to depends on till get_db is not succesful is not going to start
    
    
    return {"data": posts}


@app.get("/posts") #to retrieve all posts
def get_posts(db: Session = Depends(get_db)):
    posts=db.query(models.PostORM).all() #models=tables
    #print(posts)
    return{"data": posts} #passing the variable



#creating a post WITH PARAMETERIZED query (%s) in case in a future we need to change smthing easier

#Additionally, the posts variable here , is a dictionary because we are using RalDictCursor hence to acces the values:
#Title: {post['title']}

#we still using the pydantic class created above (Post)
@app.post("/posts", status_code=status.HTTP_201_CREATED) #adding the post to a dict and to the my_post array of dict
def create_posts(new_post: Post, db: Session = Depends(get_db)): #function expects new_post param. compliance with pydantic Post class


    #post = models.PostORM(title=new_post.title, content=new_post.content, published=new_post.published)
    post=models.PostORM(**new_post.dict())# This way we unpack the dictionary and put it in the same format the line above automatically
    db.add(post)
    db.commit()
    db.refresh(post)

    #return {"message_from_server": f"New post added!  Title: {post.title}"}
    return {"Data": {post}}
#   
         
        
 #retrieving post by id           
       
@app.get("/posts/{id}")  # Get post per id (decorator/path parameter)
def get_post(id: int, db: Session = Depends(get_db)):#performing validation with fast api we are saying I want an integer as input.
    post = db.query(models.PostORM).filter(models.PostORM.id == id).first() #first entrance that matches
    print(post)
    # cursor.execute("""SELECT * FROM posts WHERE id=%s""",(str(id)))#then we convert it to string for the query
    # post=cursor.fetchone()


    if post: #in python not empty values are considered as true same as: if post != {} (si no esta vacio... damelo else error)
        return {"post_info": {post}}  # Returns the entire post if found
    else:#if not found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": f"Post with ID: {id} not found "})
        


@app.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db) ):
    # cursor.execute("""DELETE FROM POSTS WHERE id=%s Returning *""",(str(id)))
    # post=cursor.fetchone()
    # conn.commit()
    post = db.query(models.PostORM).filter(models.PostORM.id == id).first()

    if post:
        db.delete(post)
        db.commit()
        
        raise HTTPException(status_code=status.HTTP_200_OK,detail={"info": f"Post with title: {post.title} and ID: {post.id} Succesfully deleted"})
        
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": f"Post with ID: {id} not found"} )
    
# GETTING THE ID AND PASSING THE VALUES TO BE UPDATED
@app.put("/posts/{id}")
def update_post(id: int, entry: Post):
    cursor.execute("""UPDATE posts SET title =%s, content=%s, published=%s WHERE id=%s RETURNING *""",(entry.title,entry.content,entry.published,(str(id))))
    post=cursor.fetchone()
    conn.commit()
    if post:#IF post is not none raise 200 else 404
        
        raise HTTPException(status_code=status.HTTP_200_OK, detail={"info": f"Post: {id},{post} Succesfully updated"})
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": f"Post with ID: {id} not found"})





