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
        except IntegrityError:
            raise HTTPException (status_code=403,detail="Post already liked")


            

    

    


