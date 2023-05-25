import uuid
from sqlalchemy.orm import Session
from fastapi import APIRouter
from ..database import SessionLocal
from .. import schemas, database, models,utils
from ..oauth2 import create_token,get_current_user
from fastapi import  Depends, Header, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer

oauth2_scheme =OAuth2PasswordBearer(tokenUrl='login')

router = APIRouter()

#LOGIN
@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # user = db.query(models.User).filter(models.Email.email == user_credentials.username and models.Email.id== models.User.email_id).first()
    user = db.query(models.User).join(models.Email).filter(models.Email.email == user_credentials.username, models.Email.id== models.User.email_id).first()
    if not user :
        raise HTTPException(detail= 'invalid credentials', status_code=status.HTTP_403_FORBIDDEN)
 
    if not utils.verify(user_credentials.password,user.password):
       raise HTTPException(detail= 'invalid credentials', status_code=status.HTTP_403_FORBIDDEN)
    
    token, expiration_time = create_token()
    token_db = models.AccessToken(token=token, user_id=user.id, expiration_time=expiration_time)
    db.add(token_db)
    db.commit()
    db.refresh(token_db)
    user.is_active=True
    db.commit()
    return {"access_token" : token, "token_type": "bearer"}

#email verify
@router.post('/email_verify', response_model=schemas.Token)
def email_verify(email : schemas.Email, db: Session = Depends(database.get_db)):
    email_query = db.query(models.Email).filter(models.Email.email == email.email)
    #if email is not in db create a email
    if not email_query.first():
     new_email = models.Email(**email.dict())
     db.add(new_email)
     db.commit()
    #get email data
    email_data = email_query.first()

    user_data = db.query(models.User).filter(models.User.email_id==email_data.id).first()
    if user_data:
     raise HTTPException(detail= 'user already exists', status_code=status.HTTP_409_CONFLICT)
    
    #create token
    token = str(uuid.uuid4())
    token_data = db.query(models.VerifyToken).filter(models.VerifyToken.email_id == email_data.id).first()
    if token_data:
     token_data.token = token
     token_data.is_active = True
     db.commit()
     return {"access_token" : token, "token_type": "bearer"}
    
    #if email id is not in the verify token db 
    new = models.VerifyToken(token = token, email_id = email_data.id, is_active = True)
    db.add(new)
    db.commit()
    return {"access_token" : token, "token_type": "bearer"}

#forgot passwword
@router.post('/forgot_password',  response_model=schemas.Token)
def forgot_password(email : schemas.Email, db: Session = Depends(database.get_db)):
    data = db.query(models.Email).filter(models.Email.email == email.email).first()
    if not data :
         raise HTTPException(detail= 'invalid credentials', status_code=status.HTTP_403_FORBIDDEN)
    email_id = data.id
    
    user = db.query(models.User).filter(models.User.email_id==email_id).first()
    if not user:
         raise HTTPException(detail= 'invalid credentials', status_code=status.HTTP_403_FORBIDDEN)
   
    token = str(uuid.uuid4())
    token_data = db.query(models.VerifyToken).filter(models.VerifyToken.email_id == email_id).first()
    if token_data:
     token_data.token = token
     token_data.is_active = True
     db.commit()
     return {"access_token" : token, "token_type": "bearer"}
    #if email id is not in the verify token db
    new = models.VerifyToken(token = token, email_id = data.id, is_active = True)
    db.add(new)
    db.commit()
    return {"access_token" : token, "token_type": "bearer"}

# Example usage:
@router.get('/protected')
def protected_route(user = Depends(get_current_user)):
    return {'user_id': user.id}



