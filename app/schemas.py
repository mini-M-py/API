from pydantic import BaseModel, EmailStr
from datetime import datetime
from  typing import Optional
from pydantic.types import conint
class PostBase (BaseModel):
    id: int
    title: str
    content: str
    published: bool = True



class PostCreate(PostBase):

    pass
class user_response(BaseModel):
    id : int
    user_name: str
    created_at : datetime

    class Config:
        orm_mode = True


class Post(PostBase):
    owner_id :int
    owner:user_response
    class Config:
        orm_mode = True
class VoteOut(BaseModel):
    Post: Post
    voted: bool
    votes: int
    class Config:
        orm_mode = True



class CreatePost(PostBase):
    id: int
    owner_id: int
    class Config:
        orm_mode = True


class create_user(BaseModel):
    user_name:str
    email: EmailStr
    password : str
    otp:str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    user_name: str
    created_at: datetime
    class Config:
        orm_mode = True

class OutUser(BaseModel):
    id: int
    user_name: str
    created_at: datetime
    class Config:
        orm_mode = True

class userLogin(BaseModel):
    email: EmailStr
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str

class Token_data(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

class Comment(BaseModel):
    post_id: int
    comment: str

class CommentOut(BaseModel):
    user: OutUser
    comments: str

    class Config:
        orm_mode = True

class Comment_Update(BaseModel):
    post_id: int
    comments : str

class verify(BaseModel):
    email:EmailStr
