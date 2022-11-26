from datetime import datetime
from fastapi import FastAPI, Body, HTTPException, status
from pydantic import BaseModel
from random import randrange
from uuid import uuid4
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    post_timestamp: datetime | None = None
    published: bool = True
    rating: int | None = None


try:
    conn = psycopg2.connect(host='localhost', dbname='fast-api',
                            user='postgres', password='Super#959budda2!@', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print('Databse connection was successfull!')

except Exception as e:
    print(e)


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "Favorite Foods", "content": "I like pizza", "id": 2}]


def find_index_for_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Welcome to my API!"}


@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts")
    records = cursor.fetchall()
    return {"data": records}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Post):
    print(new_post.dict())
    post_dict = new_post.dict()
    post_dict['id'] = randrange(10, 1000000)
    my_posts.append(post_dict)
    return {"new_post": post_dict}


@app.get("/posts/{id}")
def get_single_post(id: int):
    if id < 0 or id > len(my_posts):
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Post  {id} does not exist")
    else:
        for post in my_posts:
            if post['id'] == id:
                return {"message": f"post info: {post}  "}

        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Post  {id} does not exist")


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    if id < 0 or id > len(my_posts):
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Post  {id} does not exist")
    else:
        for post in my_posts:
            if post['id'] == id:
                my_posts.remove(post)
                return {"message": f"post {post} successfully deleted. "}
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Post  {id} does not exist")


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_for_post(id)
    if id < 0 or id > len(my_posts):
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Post  {id} does not exist")
    else:
        post_dict = post.dict()
        post_dict['id'] = id
        my_posts[index] = post_dict
        return {"message": post_dict}
