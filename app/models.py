from .database import Base
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey,DateTime,Date
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
# from werkzeug.security import check_password_hash


class Email(Base):
     __tablename__ = "emails"
     id = Column(Integer, primary_key=True)
     email = Column(String, nullable=False, unique=True)

class VerifyToken(Base):
    __tablename__ = "verify_tokens"
    id = Column(Integer, primary_key=True)
    email_id = Column(Integer, ForeignKey("emails.id", ondelete="CASCADE"), nullable=False)
    token = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, server_default='True')
    # expiration_time = Column(DateTime, default=datetime.utcnow)
    
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key= True, nullable=False)
    email_id = Column(Integer, ForeignKey("emails.id", ondelete="CASCADE"), nullable=False,unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    created_on = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_on =  Column(DateTime)
    phone_number = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, server_default='True')
    
class UserDetail(Base):
    __tablename__ = "user_details"
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    bio = Column(String)
    image_url =  Column(String)
    gender = Column(String, nullable=False)
    address = Column(String, nullable=False)
    created_on = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_on =  Column(DateTime)

class AccessToken(Base):
    __tablename__ = "access_tokens"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    expiration_time = Column(DateTime)
    is_active = Column(Boolean, nullable=False, server_default='True')















# class Token(Base):
#     __tablename__ = "tokens"

#     id = Column(Integer, primary_key=True, index=True)
#     uuid = Column(String, unique=True, index=True)
#     expires_at = Column(DateTime)

#     def is_expired(self) -> bool:
#         return datetime.utcnow() >= self.expires_at
    
# class UUIDToken(Base):
#     __tablename__ = "uuid_tokens"
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, index=True)
#     token = Column(String(36), default=str(uuid.uuid4()))


# class Session(Base):
#     __tablename__ = "sessions"

#     id = Column(String(36), primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     # user = relationship("User")
#     expires = Column(DateTime)

