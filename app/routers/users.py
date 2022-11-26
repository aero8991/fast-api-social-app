from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from .. import models, utils
from sqlalchemy.orm import Session
from app.database import  get_db
from app.schemas import UserResponse, UserCreate
from sqlalchemy.sql import func

router = APIRouter(
    prefix="/users",
    tags=['Users']

)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    # hash the password!
    hashed_password = utils.bcrypt_hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    # title=new_post.title, content=new_post.content, published= new_post.published ..... unpack a dictionary !
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # this is the same thing as * returning
    return new_user


@router.get("/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    #user = db.query(models.User).filter(models.User.id == id).first()

    vote_user = db.query(models.User.id, models.User.email, func.count(
        models.Post.id).label('user_post_count')).join(models.Post, models.User.id == models.Post.user_id, isouter=True)\
        .group_by(models.User.id).filter(models.User.id == id).first()
    print(vote_user)

    if not vote_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")
    return vote_user


