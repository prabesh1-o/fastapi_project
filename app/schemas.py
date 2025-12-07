from pydantic import BaseModel,EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    id:int
    email:EmailStr

    class Config:
        from_attributes = True # alllows pydantic tp read data from orm

class Token(BaseModel):
    access_token:str
    token_type:str

class TaskCreate(BaseModel):
    title:str
    description:Optional[str]=None

class TaskUpdate(BaseModel):
    status:str

class TaskResponse(BaseModel):
    id:int
    title:str
    description:Optional[str]
    status : str

    class Config:
        from_attributes = True

        