from fastapi import APIRouter, Depends,status,HTTPException,Response
from  sqlalchemy.orm import Session
from .. import database,schemas,oauth,models
from sqlalchemy.exc import IntegrityError


router=APIRouter(
    prefix="/vote"
)

@router.post("/") # el path es /vote
def vote(vote_info:schemas.Vote,db: Session = Depends(database.get_db),
         current_user:str=Depends(oauth.get_current_user)):
    if vote_info.like==1:
        try:
            vote=models.Vote(user_id=current_user.id,post_id=vote_info.post_id)
            db.add(vote)
            db.commit()
            db.refresh(vote)# Required if you want to rerurn it.
            return vote
        except IntegrityError as e:
            pgcode = getattr(e.orig, "pgcode", None)#accede al tributo pgcode 
            #Error returned by psycopg when the post does not exist  (foreign key violation)
            if pgcode == "23503":
                raise HTTPException(status_code=404,detail="Post no longer available")
            #FALLBACK like having an else
            raise HTTPException (status_code=403,detail="Post already liked")

            
        
    if vote_info.like==0:
        query=db.query(models.Vote).filter(models.Vote.user_id==current_user.id,models.Vote.post_id==vote_info.post_id).first()
        if not query:
            raise HTTPException (status_code=404,detail="U havent Liked this post")
        
        db.delete(query)
        db.commit()
        return {"Info" :"Like removed succesfully"}


            

    

    


