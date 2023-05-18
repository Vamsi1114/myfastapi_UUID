from pydantic import BaseModel,EmailStr, validator
from datetime import datetime,date
from typing import Optional



class Create_Account(BaseModel):
    first_name : str
    last_name : str
    password : str
    date_of_birth : date
    phone_number  : str

class UserOut(BaseModel):
    id : int    
    email_id: int
    created_on : datetime

    class Config:
        orm_mode = True
        
class UserLogin(BaseModel):
    email : EmailStr
    password : str

class Email(BaseModel):
    email : EmailStr

class Change_password(BaseModel):
    email : EmailStr
    old_password : str
    new_password : str

class profile(BaseModel):
    
    bio : Optional[str]
    image_url: Optional[str]

class Password(BaseModel):
    password : str


# class Edit_profile(BaseModel):
#     first_name : Optional[str]
#     last_name : Optional[str]
#     bio : Optional[str]
#     profile_pic_url: Optional[str]



# class MyModel(BaseModel):
#   foobar: datetime
  
#   @validator('foobar', pre=True)
#   def parse_foobar(cls, v):
#     if isinstance(v, str):
#       return datetime.strptime # maybe needs try/except
    # return v