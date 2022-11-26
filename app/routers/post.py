from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from .. import models, oauth2
from sqlalchemy.orm import Session
from app.database import get_db
from typing import List
from app.schemas import PostCreate, Response, PostVoteOutput, UserResponse_no_vote_info
from typing import Optional
from ..config import settings
from sqlalchemy.sql import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# , response_model=List[PostVoteOutput]


@router.get("/", response_model=List[PostVoteOutput])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
limit:int = 10, skip: int =  0, search: Optional[str]= ""):
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() # modify to specific users post (we want the user_id not the id of the post)
    # # .filter(models.Post.user_id == current_user.id).all() **
    # print(posts)
    # print(limit) # to add spaces uses %20 *****************

    posts = db.query(models.Post, func.count(
        models.Votes.post_id).label('total_votes')).join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True)\
            .group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    # votes_given = db.query(models.Votes.user_id, func.count(
    #     models.Votes.user_id).label('vote_count')).group_by(models.Votes.user_id).filter(models.Votes.user_id ==models.User.id).all()
    # print(votes_given)
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Response)
def create_posts(new_post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *""",
    #             (new_post.title, new_post.content, new_post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # instead of typing out manaual fields
    print(current_user.id)
    print(current_user.email)
    new_post = models.Post(user_id = current_user.id, **new_post.dict()) # now we are no longer adding an owner id, but we know who the current user is! current user is the one logged in! 
    # we have access to that info w/ current_user! 
    # title=new_post.title, content=new_post.content, published= new_post.published ..... unpack a dictionary !
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # this is the same thing as * returning
    return new_post


@router.get("/{id}", response_model=PostVoteOutput)
def get_single_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("SELECT * FROM posts WHERE id= %s", (str(id),))
    # post = cursor.fetchone()
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(
        models.Votes.post_id).label('total_votes')).join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True)\
        .group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Post  {id} does not exist")
    # doesnt like f strings for some reason!
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("DELETE FROM posts WHERE id= %s returning *", (str(id),))
    # post = cursor.fetchone()
    # conn.commit()
    delete_post = db.query(models.Post).filter(models.Post.id == id)
    
    delete_post_query = delete_post.first()

    if delete_post_query == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Post  {id} does not exist")
    if delete_post_query.user_id == current_user.id:

        delete_post.delete(synchronize_session=False)
        db.commit()
        return {"message": f"post deleted: {id}  "}
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"You can not delete this post")


@router.put("/{id}", response_model=Response)
def update_post(id: int, refreshed_post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s returning *",
    #                (post.title, post.content, post.published , (str(id),)))
    # updated_post = json.dumps(cursor.fetchone(), default=str)
    # conn.commit()
    # print(updated_post)
    updated_post = db.query(models.Post).filter(models.Post.id == id)
    updated_post_query = updated_post.first()

    if updated_post_query == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Post  {id} does not exist")
    #new_post = models.Post(**post.dict())
    if updated_post_query.user_id == current_user.id:
        updated_post.update(refreshed_post.dict(), synchronize_session=False)
        db.commit()
        return updated_post.first()

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=f"You can not modify this post")

    
