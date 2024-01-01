from fastapi import APIRouter, Response
from pydantic import BaseModel, UUID4
from datetime import datetime, timedelta

from jose import JWTError, jwt
import uuid, json
from schemas import admin_list

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()

class AdminLogin(BaseModel):
    username: str
    password: str

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/login/", tags=["login"])
async def login(admin: AdminLogin):
     for _admin in admin_list:
        if _admin.username == admin.username and _admin.password == admin.password:
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": admin.username}, expires_delta=access_token_expires
            )
            res = Response(json.dumps({"access_token": access_token, "token_type": "bearer"}))
            res.headers['Content-Type'] = 'application/json'
            return res
            # return {"message": "Login successful"}