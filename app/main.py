from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from . import models, oauth2
from app.database import engine
from .routers import post, users, auth, vote
from app.config import settings


#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    alow_methods=['*'],
    allow_headers=['*']
)


#import routes from seperate folder/files
app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root(get_current_user: int = Depends(oauth2.get_current_user)):
    return {"message": "Welcome to my API!"}



   