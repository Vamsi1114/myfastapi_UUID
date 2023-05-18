import uuid
from datetime import datetime, timedelta
from fastapi import  Depends, Header, HTTPException
from sqlalchemy.orm import Session
from . import database, models
from fastapi import APIRouter,status
from fastapi.security import OAuth2PasswordBearer
from .database import SessionLocal
# from .config import settings

db = SessionLocal()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

router = APIRouter()

# Generate a new UUID token for a user with an expiration time
def create_token():
    token = str(uuid.uuid4())
    expiration_time = datetime.now() + timedelta(minutes=3)
    return token, expiration_time
    
def token_check(token:str, credentials_exception):
    # Check if token is of type UUID, return exception
    try:
        uuid.UUID(token)
    except ValueError:
        return credentials_exception

    # If yes, query against Token table
    token_db = db.query(models.Token).filter(models.Token.token == token, models.Token.is_active == True).first()
    if token_db is None:
        raise credentials_exception

    # If expiration time is in the past, return exception
    if datetime.now() > token_db.expiration_time:
        return credentials_exception

    return token_db

# Get the expiration time of a UUID token
def get_token_expiration(token):
    token_db = db.query(models.Token).filter(models.Token.token == token).first()
    if token_db is None:
        return None
    else:
        return token_db.expiration_time

# Get the user ID associated with a UUID token
def get_current_user(token:str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    token_db = token_check(token, credential_exception)
        
    # If user not found with token, return exception
    user = db.query(models.User).filter(models.User.id == token_db.user_id,models.User.is_active==True).first()
    if user is None:
       raise credential_exception
    
    token_db.expiration_time = token_db.expiration_time + timedelta(minutes=2)
    db.commit()

    return user



















# Verify that a UUID token is valid and has not expired
# def verify_token(token):
#     # Check if the token is valid
#     try:
#         uuid.UUID(token)
#     except ValueError:
#         return False

#     # Check if the token has expired
#     expiration_time = get_token_expiration(token)
#     if expiration_time is None:
#         return True
#     else:
#         return datetime.now() <= expiration_time

# Example login route that generates a UUID token for a user
# @router.post('/login')
# def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
#     user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
#     token, expiration_time = create_token(user.id)
#     token_db = models.Token(token=token, user_id=user.id, expiration_time=expiration_time)
#     db.add(token_db)
#     db.commit()
#     db.refresh(token_db)
#     return {'token': token}

# # Example usage:
# @router.get('/protected')
# def protected_route(user = Depends(get_current_user)):
#     return {'user_id': user.id}










# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from uuid import UUID, uuid4
# from datetime import datetime, timedelta
# from . import models, schemas, database
# from .database import get_db


# router = APIRouter()

# # Example of a dependency to get the database session
# def get_db():
#     db = database.SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # # Example of a dependency to authenticate a user
# def authenticate_user(db: Session, username: str, password: str):
#     user = db.query(models.User).filter(models.User.email == username).first()
#     if not user or not user.check_password(password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid credentials"
#         )
#     return user

# # # Example of a dependency to get a session
# def get_session(db: Session, session_id: UUID):
#     session = db.query(models.Session).filter(models.Session.id == session_id).first()
#     if not session or session.expires < datetime.utcnow():
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid session"
#         )
#     return session

# # # Example of a login endpoint to create a session
# @router.post("/login")
# def login(
#     request: schemas.UserLogin,
#     db: Session = Depends(get_db)
# ):
#     user = authenticate_user(db, request.email, request.password)
#     session_id = uuid4()
#     session_expires = datetime.utcnow() + timedelta(hours=2)
#     session = models.Session(id=session_id, user_id=user.id, expires=session_expires)
#     db.add(session)
#     db.commit()
#     db.refresh(session)
#     return {"session_id": session_id}

# # # Example of a protected endpoint that requires authentication
# # @router.get("/protected")
# # def protected(
# #     session: models.Session = Depends(get_session),
# #     db: Session = Depends(get_db)
# # ):
# #     user = db.query(models.User).filter(models.User.id == session.user_id).first()
# #     return {"message": f"Hello, {user.user_name}!"}
