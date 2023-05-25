from fastapi import Depends,status,HTTPException,APIRouter
from app import models
from ..database import get_db
from app import schemas
from sqlalchemy.orm import Session
from ..oauth2 import get_current_user
from datetime import datetime

router = APIRouter()

#create user profile
@router.post("/profile",status_code=status.HTTP_201_CREATED)
def create_profile(data : schemas.profile, db:Session = Depends(get_db), user: models.User = Depends(get_current_user)):
  
  data_query = db.query(models.UserDetail).filter(models.UserDetail.user_id == user.id).first()

  if data_query :
    raise HTTPException(detail= 'user profile already exists', status_code=status.HTTP_409_CONFLICT)
  new = models.UserDetail(user_id = user.id, **data.dict())
  db.add(new)
  db.commit()
  db.refresh(new)
  return new

#edit user profile
@router.put("/edit_profile")
def edit_profile(data : schemas.profile, db:Session = Depends(get_db), user: models.User = Depends(get_current_user)):
  
  query = db.query(models.UserDetail).filter(models.UserDetail.user_id == user.id)
  query.update(data.dict())
  db.commit()
  data = query.first()
  data.updated_on = datetime.now()
  db.commit()
  return {"Message" : "Profile updated"}

