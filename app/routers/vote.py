from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from .. import models, oauth2
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import PostCreate, Response, Vote_view
from sqlalchemy import func

router = APIRouter(
    prefix="/vote",
    tags=['Vote system']

)

@router.post("/", status_code=status.HTTP_201_CREATED)
def modify_vote(post: Vote_view, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    #if (Vote_view.dir == 1):
    #new_vote = models.Votes(**post.dict())
    user_check = db.query(models.Votes).filter(
            models.Votes.user_id == current_user.id, models.Votes.post_id == post.post_id)
    found_vote = user_check.first()
    post_checker = db.query(func.max(models.Votes.post_id)).scalar() # scaler returns the first value !!!!  I could also just check if it exists or not :) 
    #(thats probably easier)
    if post.post_id > post_checker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist.")
    if (post.dir == 1):

        if found_vote:
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail=f"Already voted on this post!")
        new_vote = models.Votes(post_id = post.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        user_check.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}


    
