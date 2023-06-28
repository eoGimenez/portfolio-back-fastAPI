import os
from datetime import datetime, timedelta
from passlib.context import CryptContext
import jwt
from fastapi import APIRouter, Security, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from models.user import User
from db.config import db_client

router = APIRouter(prefix='/api/auth', tags=['Auth'])


class AuthHandler():
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bycrypt"], deprecated="auto")
    secret = os.environ.get("SECRET")

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, user_id):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, minutes=5),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401, detail='Signature has expired')
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail='Invalid credentials')

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)
# @router.post('/signup')
# async def create_user(form: OAuth2PasswordRequestForm = Depends()):
#     if isinstance(db_client.fastAPIDOS.users.get(form.email)):
#         return {"message": "El usuario ya existe"}
#     hashed_pass = bcrypt.encrypt(form.password)
#     db_client.fastAPIDOS.users.insert_one(
#         {"email": form.email, "password": hashed_pass, "userName": form.username})
