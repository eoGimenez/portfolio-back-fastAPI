import os
from datetime import datetime, timedelta
from passlib.context import CryptContext
import jwt
from fastapi import APIRouter, Depends, Security, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from models.user import user
from db.config import db_client

router = APIRouter(prefix='/api/auth', tags=['Auth'])


class AuthHandler():
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = os.environ.get("SECRET")

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, user_id):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=1),
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


auth_handler = AuthHandler()


@router.post('/signup', status_code=201)
async def create_user(user_details: user.User):
    if db_client.test.users.find_one({"email": user_details.email}):
        raise HTTPException(
            status_code=400, detail='User is already regitered')
    hashed_pass = auth_handler.get_password_hash(user_details.password)
    db_client.test.users.insert_one(
        {"email": user_details.email, "password": hashed_pass, "username": user_details.username})
    return {"message": "creado wach"}


@router.post('/login', status_code=200)
async def login_user(user_details: user.User):
    user = db_client.test.users.find_one({"email": user_details.email})
    if (not user or (not auth_handler.verify_password(user_details.password, user['password']))):
        raise HTTPException(status_code=401, detail='Wrong credencials')
    token = auth_handler.encode_token(user['email'])
    return {'token': token}


@router.get('/verify', status_code=201)
async def verify_token(email=Depends(auth_handler.auth_wrapper)):
    user_tok: user.User = db_client.test.users.find_one({"email": email})
    return user.User(**user_tok)
