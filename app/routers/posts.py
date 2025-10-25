from fastapi import FastAPI, Response, status, HTTPException, Depends,APIRouter
from .. import schemas,models,database,oauth
from  sqlalchemy.orm import Session
from typing import Optional, List
from datetime import date, datetime, time
from sqlalchemy import func,select
from fastapi.encoders import jsonable_encoder

router= APIRouter(
    prefix="/posts",
    tags=['posts'] # This is mainly for improveing the readability of http://localhost:8000/docs
)

# RETRIEVE ALL POSTS

@router.get("/",response_model=List[schemas.PostVotes]) #to retrieve all posts list is required
#@router.get("/")
def get_posts(db: Session = Depends(database.get_db),user_id:int=Depends(oauth.get_current_user),search:Optional[str] ="",limit:Optional[int]=10):
    
    posts=(db.query(models.PostORM).filter(models.PostORM.title.contains(search))
           .limit(limit).all()) #models=tables
    # Posts with Votes

    stmt = (
    select(models.PostORM, func.count(models.Vote.post_id).label("Likes"))
    .outerjoin(models.Vote, models.Vote.post_id == models.PostORM.id)
    .group_by(models.PostORM.id)
    )
    if search:
        stmt=stmt.where(models.PostORM.title.contains(search))
    rows = db.execute(stmt).mappings().all()  # De esta forma se convierten las tuplas/instancias ORM  a dicts y podemos hacer el return
    
    return rows 

    #return results

#RETIEVE POSTS BASED IN DATE AND SEARCH (TITLE) QUERY
#@router.get("/date",response_model=List[schemas.PostResponse])
@router.get("/date") #to retrieve all posts list is required
def get_posts(
    db: Session = Depends(database.get_db),
   # user_id:int=Depends(oauth.get_current_user),
    search:Optional[str] ="",
    day_start:Optional[date]=None,day_end:Optional[date]=None):

    start_dt = datetime.combine(day_start, time.min) if day_start else None   # 2025-09-12 00:00:00
    end_dt   = datetime.combine(day_end,   time.max) if day_end   else None   # 2025-09-13 23:59:59.999999
    
    stmt = (
    select(models.PostORM, func.count(models.Vote.post_id).label("Likes"))
    .outerjoin(models.Vote, models.Vote.post_id == models.PostORM.id).order_by(models.PostORM.created_at.desc()).
    group_by(models.PostORM.id)
    )

    if start_dt:
        stmt = stmt.where(models.PostORM.created_at >= start_dt)
    if end_dt:
        stmt = stmt.where(models.PostORM.created_at <= end_dt)
    
    if search:
        stmt=stmt.where(models.PostORM.title.contains(search))#search by title


    print(stmt)
    results=db.execute(stmt).mappings().all()
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No posts found for the provided paramenters")

    
    return results #removing the dict and retunr the stuff  no data keyword
# RETRIEVE USER POSTS

@router.get("/my-posts",response_model=List[schemas.PostVotes]) #to retrieve all posts list is required
def get_posts(db: Session = Depends(database.get_db),search:Optional[str]="", current_user:int=Depends(oauth.get_current_user)):
    
    

    stmt = (
    select(models.PostORM, func.count(models.Vote.post_id).label("Likes"))
    .outerjoin(models.Vote, models.Vote.post_id == models.PostORM.id).where(models.PostORM.title.contains(search))
    .group_by(models.PostORM.id)
    )
    print(current_user.id)
    stmt=stmt.where(models.PostORM.user_id==current_user.id)
    rows = db.execute(stmt).mappings().all()  # De esta forma se convierten las tuplas/instancias ORM  a dicts y podemos hacer el return
    
    
    
    if not rows:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="You have no posts ADD one!.🤩")
    
    return rows 
        

#we still using the pydantic class created above (Post)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse) #adding the post to a dict and to the my_post array of dict
def create_posts(new_post: schemas.Post, db: Session = Depends(database.get_db),current_user:str=Depends(oauth.get_current_user)): #function expects new_post param. compliance with pydantic Post class

    
    #post = models.PostORM(title=new_post.title, content=new_post.content, published=new_post.published)
    #new_post.user_id=int(current_user.id) we are getting the user_id value from the token to identify the user/creator
    post=models.PostORM(user_id=current_user.id,**new_post.dict())# This way we unpack the dictionary and put it in the same format the line above automatically
    
    db.add(post)
    db.commit()
    db.refresh(post)

    #return {"message_from_server": f"New post added!  Title: {post.title}"}
    return post
#   
         
        
 #retrieving post by id           
#@router.get("/{id}")       
@router.get("/{id}",response_model=List[schemas.PostVotes])  # Get post per id (decorator/path parameter)
def get_post(id: int, db: Session = Depends(database.get_db)):#performing validation with fast api we are saying I want an integer as input.
   
    post = db.query(models.PostORM).filter(models.PostORM.id == id).first() #first entrance that matches
    stmt = (
    select(models.PostORM, func.count(models.Vote.post_id).label("Likes"))
    .outerjoin(models.Vote, models.Vote.post_id == models.PostORM.id).where(models.PostORM.id==id)
    .group_by(models.PostORM.id)
    )
    

    result=db.execute(stmt).mappings().all()
    if result: #in python not empty values are considered as true same as: if post != {} (si no esta vacio... damelo else error)
        return result  # Returns the entire post if found
    else:#if not found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": f"Post with ID: {id} not found "})
        


@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(database.get_db),current_user:str=Depends(oauth.get_current_user) ):
   
    post = db.query(models.PostORM).filter(models.PostORM.id == id).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} not found") #First we check the existence

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Operation not allowed")

    db.delete(post)
    db.commit()
    
    return {"info": f"Post with title: {post.title!r} and ID: {post.id!r} successfully deleted"}
    
    
# GETTING THE ID AND PASSING THE VALUES TO BE UPDATED
@router.put("/{id}",response_model=schemas.PostResponseUpdate)
def update_post(id: int, entry: schemas.PostUpdate,db: Session = Depends(database.get_db),current_user:str=Depends(oauth.get_current_user)): #Post is the pydacntic class
    # CONSULTA - tiene método .update() para operaciones masivas
    post_query=db.query(models.PostORM).filter(models.PostORM.id == id)#query object, can call an .update method (bulk) it does not execute nothing yet
    # INSTANCIA ORM - NO tiene .update(), se modifican atributos directamente 
    post=post_query.first() #nos permite recuperar el objeto
    
    if not post: #First we check the existence
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {id} not found"
        )

    # 2. Compruebo autorización
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not permitted to update this post"
        )

    # 3. Actualizo, confirmo y devuelvo
    post_query.update(entry.dict(), synchronize_session=False)# Genera el cambio en la sesion  hastga que se genera el commit
    db.commit()# Hace durable el cambio
    db.refresh(post)  
    return post



