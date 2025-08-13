
######
#using Pydantic
######

from typing import Optional, List
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
from . import schemas


models.Base.metadata.create_all(bind=engine)

app=FastAPI() #create instance of fastapi





@app.get("/")#the route where to find the stuff /fran would be: http://127.0.0.1:8000/fran (decorator , endpoint)
def root(): #root=funtion name (does not matter)
    return {"message": "Hello World"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)): #thanks to depends on till get_db is not succesful is not going to start
    
    posts=db.query(models.PostORM).all()
    
    return {"data": posts}


@app.get("/posts",response_model=List[schemas.PostResponse]) #to retrieve all posts
def get_posts(db: Session = Depends(get_db)):
    posts=db.query(models.PostORM).all() #models=tables
    
    return posts #removing the dict and retunr the stuff  no data keyword



#creating a post WITH PARAMETERIZED query (%s) in case in a future we need to change smthing easier

#Additionally, the posts variable here , is a dictionary because we are using RalDictCursor hence to acces the values:
#Title: {post['title']}

#we still using the pydantic class created above (Post)
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse) #adding the post to a dict and to the my_post array of dict
def create_posts(new_post: schemas.Post, db: Session = Depends(get_db)): #function expects new_post param. compliance with pydantic Post class


    #post = models.PostORM(title=new_post.title, content=new_post.content, published=new_post.published)
    post=models.PostORM(**new_post.dict())# This way we unpack the dictionary and put it in the same format the line above automatically
    db.add(post)
    db.commit()
    db.refresh(post)

    #return {"message_from_server": f"New post added!  Title: {post.title}"}
    return post
#   
         
        
 #retrieving post by id           
       
@app.get("/posts/{id}",response_model=schemas.PostResponse)  # Get post per id (decorator/path parameter)
def get_post(id: int, db: Session = Depends(get_db)):#performing validation with fast api we are saying I want an integer as input.
    post = db.query(models.PostORM).filter(models.PostORM.id == id).first() #first entrance that matches
    #print(post)
    # cursor.execute("""SELECT * FROM posts WHERE id=%s""",(str(id)))#then we convert it to string for the query
    # post=cursor.fetchone()


    if post: #in python not empty values are considered as true same as: if post != {} (si no esta vacio... damelo else error)
        return post  # Returns the entire post if found
    else:#if not found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": f"Post with ID: {id} not found "})
        


@app.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db) ):
   
    post = db.query(models.PostORM).filter(models.PostORM.id == id).first()

    if post:
        db.delete(post)
        db.commit()
        
        raise HTTPException(status_code=status.HTTP_200_OK,detail={"info": f"Post with title: {post.title} and ID: {post.id} Succesfully deleted"})
        
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": f"Post with ID: {id} not found"} )
    
# GETTING THE ID AND PASSING THE VALUES TO BE UPDATED
@app.put("/posts/{id}")
def update_post(id: int, entry: schemas.PostUpdate,db: Session = Depends(get_db)): #Post is the pydacntic class
    
    post_query=db.query(models.PostORM).filter(models.PostORM.id == id)#query object, can call an update (bulk)
    post=post_query.first()# used to check the existence (model instance cannot call an update)
    
    if post:#IF post is not none raise 200 else 404
        post_query.update(entry.dict(),synchronize_session=False)
        
        db.commit()
        #db.refresh(post)
        return  {post_query.first()}
        # raise HTTPException(status_code=status.HTTP_200_OK, detail={"info": f"Post: {id},{post} Succesfully updated"})
        
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": f"Post with ID: {id} not found"})




@app.post("/useradd", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse) 
def create_user(new_user: schemas.Useradd, db: Session = Depends(get_db)):
    
    
    user=models.Users(**new_user.dict())# This way we unpack the dictionary and put it in the same format the line above automatically
    db.add(user)
    db.commit()
    db.refresh(user)

    #return {"message_from_server": f"New post added!  Title: {post.title}"}
    return user

