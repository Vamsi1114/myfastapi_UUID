import uuid
from datetime import datetime, timedelta
from fastapi import  Depends, Header, HTTPException
from sqlalchemy.orm import Session
from . import database, models
from fastapi import APIRouter,status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

router = APIRouter()

# Generate a new UUID token for a user with an expiration time
def create_token():
    token = str(uuid.uuid4())
    expiration_time = datetime.now() + timedelta(minutes=3)
    return token, expiration_time
    
def token_check(token:str, credentials_exception, db:Session):
    # Check if token is of type UUID, return exception
    try:
        uuid.UUID(token)
    except ValueError:
        raise credentials_exception
    
    # If yes, query against Token table
    token_db = db.query(models.AccessToken).filter(models.AccessToken.token == token, models.AccessToken.is_active == True).first()
    if token_db is None:
        raise credentials_exception
    
    # If expiration time is in the past, return exception
    if datetime.now() > token_db.expiration_time:
        raise credentials_exception

    return token_db

# Get the user ID associated with a UUID token
def get_current_user(token:str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "could not validate credentials", headers = {"WWW-Authenticate": "Bearer"})
    token_db = token_check(token, credential_exception, db)
    
    # If user not found with token, return exception
    user = db.query(models.User).filter(models.User.id == token_db.user_id, models.User.is_active==True).first()
    if user is None:
       raise credential_exception
    
    token_db.expiration_time = token_db.expiration_time + timedelta(minutes=2)
    db.commit()

    return user




















# # Get the expiration time of a UUID token
# def get_token_expiration(token):
#     token_db = db.query(models.AccessToken).filter(models.AccessToken == token).first()
#     if token_db is None:
#         return None
#     else:
#         return token_db.expiration_time