from fastapi import FastAPI, Response, status, HTTPException, Depends,APIRouter
from .. import schemas,models,database,oauth
from  sqlalchemy.orm import Session
from typing import Optional, List

router= APIRouter(
    prefix="/posts",
    tags=['posts'] # This is mainly for improveing the readability of http://localhost:8000/docs
)

@router.get("/",response_model=List[schemas.PostResponse]) #to retrieve all posts
def get_posts(db: Session = Depends(database.get_db),user_id:int=Depends(oauth.get_current_user)):
    posts=db.query(models.PostORM).all() #models=tables
    
    return posts #removing the dict and retunr the stuff  no data keyword



#creating a post WITH PARAMETERIZED query (%s) in case in a future we need to change smthing easier

#Additionally, the posts variable here , is a dictionary because we are using RalDictCursor hence to acces the values:
#Title: {post['title']}

#we still using the pydantic class created above (Post)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse) #adding the post to a dict and to the my_post array of dict
def create_posts(new_post: schemas.Post, db: Session = Depends(database.get_db),current_user:str=Depends(oauth.get_current_user)): #function expects new_post param. compliance with pydantic Post class

    
    #post = models.PostORM(title=new_post.title, content=new_post.content, published=new_post.published)
    #new_post.user_id=int(current_user.id)
    post=models.PostORM(user_id=current_user.id,**new_post.dict())# This way we unpack the dictionary and put it in the same format the line above automatically
    
    db.add(post)
    db.commit()
    db.refresh(post)

    #return {"message_from_server": f"New post added!  Title: {post.title}"}
    return post
#   
         
        
 #retrieving post by id           
       
@router.get("/{id}",response_model=schemas.PostResponse)  # Get post per id (decorator/path parameter)
def get_post(id: int, db: Session = Depends(database.get_db)):#performing validation with fast api we are saying I want an integer as input.
    post = db.query(models.PostORM).filter(models.PostORM.id == id).first() #first entrance that matches
    #print(post)
    # cursor.execute("""SELECT * FROM posts WHERE id=%s""",(str(id)))#then we convert it to string for the query
    # post=cursor.fetchone()


    if post: #in python not empty values are considered as true same as: if post != {} (si no esta vacio... damelo else error)
        return post  # Returns the entire post if found
    else:#if not found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": f"Post with ID: {id} not found "})
        


@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(database.get_db) ):
   
    post = db.query(models.PostORM).filter(models.PostORM.id == id).first()

    if post:
        db.delete(post)
        db.commit()
        
        raise HTTPException(status_code=status.HTTP_200_OK,detail={"info": f"Post with title: {post.title!r} and ID: {post.id!r} Succesfully deleted"})
        
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": f"Post with ID: {id} not found"} )
    
# GETTING THE ID AND PASSING THE VALUES TO BE UPDATED
@router.put("/{id}",response_model=schemas.PostResponseUpdate)
def update_post(id: int, entry: schemas.PostUpdate,db: Session = Depends(database.get_db)): #Post is the pydacntic class
    
    post_query=db.query(models.PostORM).filter(models.PostORM.id == id)#query object, can call an update (bulk)
    post=post_query.first()# used to check the existence (model instance cannot call an update)
    
    if post:#IF post is not none raise 200 else 404
        post_query.update(entry.dict(),synchronize_session=False)
        
        db.commit()
        #db.refresh(post)
        return  post_query.first()
        # raise HTTPException(status_code=status.HTTP_200_OK, detail={"info": f"Post: {id},{post} Succesfully updated"})
        
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": f"Post with ID: {id} not found"})


###---------USER STUFF---------###

