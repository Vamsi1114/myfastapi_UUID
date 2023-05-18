import uuid
from fastapi import  Depends, Header, HTTPException,status
from sqlalchemy.orm import Session
from .. import schemas, database, models,utils
# from .config import settings
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from ..database import SessionLocal
from ..oauth2 import create_token,get_current_user

db = SessionLocal()

oauth2_scheme =OAuth2PasswordBearer(tokenUrl='login')


router = APIRouter()

#LOGIN
@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # user = db.query(models.User).filter(models.Email.email == user_credentials.username and models.Email.id== models.User.email_id).first()
    user = db.query(models.User).join(models.Email).filter(models.Email.email == user_credentials.username and models.Email.id== models.User.email_id).first()
    if not user :
        raise HTTPException(detail= 'invalid credentials', status_code=status.HTTP_403_FORBIDDEN)
 
    if not utils.verify(user_credentials.password,user.password):
       raise HTTPException(detail= 'invalid credentials', status_code=status.HTTP_403_FORBIDDEN)
    token, expiration_time = create_token()
    token_db = models.Token(token=token, user_id=user.id, expiration_time=expiration_time)
    db.add(token_db)
    db.commit()
    db.refresh(token_db)
    user.is_active=True
    db.commit()
    return {'access_token': token}

#email verify
@router.post('/verify')
def email_verify(email : schemas.Email, db: Session = Depends(database.get_db)):
    user_email = db.query(models.Email).filter(models.Email.email == email.email).first()
    if not user_email:
     new_user = models.Email(**email.dict())
     db.add(new_user)
     db.commit()
    email_data = db.query(models.Email).filter(models.Email.email==email.email).first()
    user_data = db.query(models.User).filter(models.User.email_id==email_data.id).first()
    if user_data  :
      raise HTTPException(detail= 'user already exists', status_code=status.HTTP_403_FORBIDDEN)
    token = str(uuid.uuid4())
    new = models.Email_verify(verify_token = token, email_id = email_data.id,is_active = True)
    db.add(new)
    db.commit()
    return {'access_token': token}

#forgot passwword
@router.post('/forgot_password')
def forgot_password(email : schemas.Email, db: Session = Depends(database.get_db), token:str = Depends(oauth2_scheme)):
    data = db.query(models.Email).filter(models.Email.email == email.email).first()
    if not data :
         raise HTTPException(detail= 'invalid credentials', status_code=status.HTTP_403_FORBIDDEN)
    email_id = data.id
    user = db.query(models.User).filter(models.User.email_id==email_id).first()
    if not user:
         raise HTTPException(detail= 'invalid credentials', status_code=status.HTTP_403_FORBIDDEN)
   
    token = str(uuid.uuid4())
    new = models.Email_verify(verify_token = token, email_id=data.id,is_active = True)
    db.add(new)
    db.commit()
    return {'access_token': token}

# Example usage:
@router.get('/protected')
def protected_route(user = Depends(get_current_user)):
    return {'user_id': user.id}







    # new_data = models.token_verify(is_active=False)
    # db.add(new_data)
    # db.commit()
    # models.token_verify.verify_token = token
    # models.token_verify.email_id = email_data.id



