from pydantic import BaseModel, EmailStr
from typing import Literal

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    #rating: int | None = None

class PostCreate(PostBase):
    pass


class UserResponse(BaseModel):
    email: EmailStr
    user_post_count: int = 0 # need to figure out how to join this back with the post count

    class Config:
        orm_mode = True


class UserResponse_no_vote_info(BaseModel): ## temp model created here drop user_post_count info
    email: EmailStr
    

    class Config:
        orm_mode = True

class Response(PostBase): #POST CLASS
    # title: str
    # content: str
    # published: bool 
    id: int
    user_id: int  #lecture uses owner_id
    owner: UserResponse_no_vote_info # built in relationship w/in pydantic. we just reference the model class! 
    #Also order matters, so we had to organize the structure and put UserReponse above
    

    class Config:
        orm_mode=True




class PostVoteOutput(BaseModel):
    Post: Response
    total_votes: int # I named it total votes

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserVoteInfo(BaseModel):
    #something: UserResponse
    pass



class LoginResponse(UserResponse):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: str | None = None

class Vote_view(BaseModel):
    post_id: int
    dir: Literal[0, 1] 

