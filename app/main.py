from fastapi import FastAPI
from app import oauth2
from .routers import users,auth,profile,pdf

app = FastAPI()

app.include_router(oauth2.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(pdf.router)

# models.Base.metadata.create_all(bind=engine) 

@app.get("/")
async def root():
    return {"message": "Hello World"}





















# #create user
# @app.post("/user",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
# def create_account(user : schemas.Create_Account,db:Session = Depends(get_db)):
  
#   #hash the password - user.password
#   password = user.password.encode('utf-8')
#   hashed_password  = utils.hash(password)
#   user.password = hashed_password

#   new_user = models.User(**user.dict())
#   print(user.dict())
#   db.add(new_user)
#   db.commit()
#   db.refresh(new_user)

#   return new_user

# #Change password
# @app.put('/user')
# def get_user(user_credentials: schemas.Change_password,db:Session = Depends(get_db),user: models.User = Depends(get_current_user)):#user: models.User = Depends(get_current_user)
#  user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

#  if not user :
#         raise HTTPException(detail= 'invalid credentials',status_code=status.HTTP_403_FORBIDDEN)
 
#  if not utils.verify(user_credentials.old_password,user.password):
#        raise HTTPException(detail= 'invalid credentials',status_code=status.HTTP_403_FORBIDDEN)
#  password = user_credentials.new_password.encode('utf-8')
#  hashed_password  = utils.hash(password)
#  user.password = hashed_password
#  user.updated_on = datetime.now()
#  db.commit()

#  return {"Message" : "Password changed sucsessfully"}
   


#login router or path operation 
# @app.post('/login')
# def login(user_credentials : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):

# #   {
# #      "username": "ggaggkag" 
# #      "password": "jhgfeuer"
# #   }
#    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

#    if not user :
#         raise HTTPException(detail= 'invalid credentials',status_code=status.HTTP_403_FORBIDDEN)
 
#    if not utils.verify(user_credentials.password,user.password):
#        raise HTTPException(detail= 'invalid credentials',status_code=status.HTTP_403_FORBIDDEN)
   
#    return {"Message" : "user login completed"}
   #we create a token 
   # return the token
#  acess_token = oauth2.create_access_token(data={"user_id":user.id, "user_email": user.email})

#  return {"access_token" : acess_token,"token_type": "bearer"}

# chanage password