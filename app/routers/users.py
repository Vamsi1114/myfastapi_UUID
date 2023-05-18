from fastapi import Depends,status,HTTPException,APIRouter
from app import models
from ..database import get_db
from app import schemas,models
from sqlalchemy.orm import Session
from app import utils
from datetime import datetime
from ..oauth2 import get_current_user
# from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme =OAuth2PasswordBearer(tokenUrl='login')

router = APIRouter()

#create user
@router.post("/user",status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_account(user : schemas.Create_Account, token:str = Depends(oauth2_scheme), db:Session = Depends(get_db)): 
  
  token_data = db.query(models.Email_verify).filter(models.Email_verify.verify_token==token, models.Email_verify.is_active==True).first()
  if not token_data :
      raise HTTPException(detail= 'Token already used', status_code=status.HTTP_403_FORBIDDEN)
  
  user_data = db.query(models.User).filter(models.User.email_id==token_data.email_id).first()
  if user_data  :
      raise HTTPException(detail= 'user already exists', status_code=status.HTTP_403_FORBIDDEN)
  
  #hash the password - user.password
  password = user.password.encode('utf-8')
  hashed_password  = utils.hash(password)
  user.password = hashed_password

  new_user = models.User(email_id = token_data.email_id, **user.dict())
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  token_data.is_active= False
  db.commit()
  return new_user

#Change password
@router.put('/change_password')
def chnage_password(user_credentials: schemas.Change_password, db:Session = Depends(get_db), user: models.User = Depends(get_current_user)):#user: models.User = Depends(get_current_user)
#  email = db.query(models.Email).filter(models.Email.email==user_credentials.email).first()
 user_data = db.query(models.User).join(models.Email).filter(models.User.email_id == user.email_id , models.Email.email == user_credentials.email).first()

 if not user_data :
        raise HTTPException(detail= 'invalid credentials', status_code=status.HTTP_403_FORBIDDEN)
 
 if not utils.verify(user_credentials.old_password,user.password):
       raise HTTPException(detail= 'invalid credentials', status_code=status.HTTP_403_FORBIDDEN)
 password = user_credentials.new_password.encode('utf-8')
 hashed_password  = utils.hash(password)
 user.password = hashed_password
 user.updated_on = datetime.now()
 db.commit()
 return {"Message" : "Password changed sucsessfully"}

#Set password 
@router.put('/set_password')
def set_password(user_credentials: schemas.Password, token:str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    token_data = db.query(models.Email_verify).filter(models.Email_verify.verify_token==token, models.Email_verify.is_active==True).first()
    # data = db.query(models.Email).join(models.token_verify).filter(models.token_verify.verify_token==token,models.Email.email == user_credentials.email).first()
    if not token_data :
         raise HTTPException(detail= 'Token already used', status_code=status.HTTP_403_FORBIDDEN)
    email_id = token_data.email_id
    user = db.query(models.User).filter(models.User.email_id==email_id).first()
    if not user:
         raise HTTPException(detail= 'invalid credentials', status_code=status.HTTP_403_FORBIDDEN)
    hash_password = utils.hash(user_credentials.password)
    user.password = hash_password
    user.updated_on = datetime.now()
    db.add(user)
    db.commit()
    token_data.is_active= False
    db.commit()
    return {"Message" : "Password changed sucsessfully"}


#LOGOUT
@router.put('/logout')
def logout(db:Session = Depends(get_db), token:str = Depends(oauth2_scheme), user: models.User = Depends(get_current_user)):
    data = db.query(models.Token).filter(models.Token.user_id==user.id, models.Token.token==token).first()
    if not data :
        raise HTTPException(detail= 'invalid credentials', status_code=status.HTTP_403_FORBIDDEN)
    data.is_active = False
    db.commit()
    return {"Message" : "You have been logged out."}

#Deactivate
@router.put('/deactivate')
def deactive_account(db:Session = Depends(get_db), user: models.User = Depends(get_current_user)):
#    if user==None:
#        raise HTTPException(detail= 'invalid credentials',status_code=status.HTTP_403_FORBIDDEN)
   user.is_active=False
   db.commit()
   return {"Message" : "Acoount deavtiveted"}