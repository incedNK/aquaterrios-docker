from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Union, List

from schema import devices

# Deals with authorisation and authentications
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
    
class Login(BaseModel):
    username: str
    password: str
    
class LostPassword(BaseModel):
    password: str
    
class ResetPassword(BaseModel):
    secret: str
    password: str

# Handle admins notifications to users
class NoteCreate(BaseModel):
    user: str
    read: bool = False
    message: str
   

class Notifications(BaseModel):
    id: int
    user: str
    message: str
    read: bool
    date: datetime
    
    class Config:
        orm_mode = True 

class UpdateNote(BaseModel):
    read: bool = True

# Handle users reads and creates
class UserBase(BaseModel):
    username: str
    email: EmailStr
    name: str
    surname: str
    address: str
    admin: bool = False
    premium: bool = False
        
    
class UserCreate(UserBase):
    password: str
    delisted: bool = True
        
class User(UserBase):
    delisted: bool
    updated_at: datetime
    created_at: datetime
    
    alerts: List[Notifications]= []
    systems: List[devices.System] = []
    
    class Config:
        orm_mode = True
        
class UserUpdate(BaseModel):
    name: Optional[str]
    surname: Optional[str]
    address: Optional[str]
    email: Optional[EmailStr]
    updated_at: datetime = datetime.now()

class AdminUserUpdate(BaseModel):
    admin: Optional[bool]
    premium: Optional[bool]
    delisted: Optional[bool]

#Subscriptions to services    
class SubscriberCreate(BaseModel):
    mail: str

class Subscribtion(SubscriberCreate):
    date: datetime
    
    class Config:
        orm_mode = True