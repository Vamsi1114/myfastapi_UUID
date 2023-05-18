from passlib.context import CryptContext
from werkzeug.security import check_password_hash
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash(password : str):
    return pwd_context.hash(password)

def verify(plain_password , hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

# def check_password(self, password):
#         return check_password_hash(self.password, password)