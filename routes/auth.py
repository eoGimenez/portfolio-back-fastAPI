import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from models.user import User
from db.config import db_client

hash_sys = "HS256"
token_life = 1
SECRET = os.environ.get("SECRET")
router = APIRouter(prefix='/api/auth', tags=['Auth'])

auth_sys = OAuth2PasswordBearer(tokenUrl='login')

bcrypt = CryptContext(schemes=["bcrypt"])


@router.post('/signup')
async def create_user(form: OAuth2PasswordRequestForm = Depends()):
    if isinstance(db_client.fastAPIDOS.users.get(form.email)):
        return {"message": "El usuario ya existe"}
    hashed_pass = bcrypt.encrypt(form.password)
    db_client.fastAPIDOS.users.insert_one(
        {"email": form.email, "password": hashed_pass, "userName": form.username})
