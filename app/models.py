from .database import Base
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey,DateTime
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
# from werkzeug.security import check_password_hash


class Email(Base):
     __tablename__ = "emails"
     id = Column(Integer, primary_key=True, index=True)
     email = Column(String, nullable=False, unique=True)

class Email_verify(Base):
    __tablename__ = "email_verify"
    id = Column(Integer, primary_key=True, index=True)
    email_id = Column(Integer, ForeignKey("emails.id",ondelete="CASCADE"), nullable=False)
    verify_token = Column(String)
    is_active = Column(Boolean, nullable=False, server_default='True')
    # expiration_time = Column(DateTime, default=datetime.utcnow)
    
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key= True, nullable=False)
    email_id = Column(Integer, ForeignKey("emails.id", ondelete="CASCADE"), nullable=False,unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    created_on = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_on =  Column(DateTime)
    phone_number = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, server_default='True')
    # is_deleted = Column(Boolean,nullable=False,server_default='False')
    # def check_password(self, password):
    #     return check_password_hash(self.password, password)

class Profile(Base):
    __tablename__ = "profile"
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    bio = Column(String)
    image_url =  Column(String)
    created_on = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_on =  Column(DateTime, default=datetime.utcnow)

class Token(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    expiration_time = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, nullable=False,server_default='True')















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

