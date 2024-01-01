from fastapi import APIRouter, HTTPException, Depends, Response, Request
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

from pydantic import BaseModel
from datetime import datetime, timedelta
import json, os
from dotenv import load_dotenv
from schemas import admin_list

router = APIRouter()
load_dotenv()

# Kunci rahasia untuk token JWT
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")

class AdminLogin(BaseModel):
    username: str
    password: str

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False
        try:
            print(jwtoken)
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return decoded_token if decoded_token["exp"] >= int(datetime.utcnow().timestamp()) else None
    except Exception as e:
        print(e)
        return {}

@router.post("/auth/", tags=["auth"])
async def login(admin: AdminLogin):
     for _admin in admin_list:
        if _admin.username == admin.username and _admin.password == admin.password:
            access_token_expires = timedelta(minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES))
            access_token = create_access_token(
                data={"sub": admin.username}, expires_delta=access_token_expires
            )
            res = Response(json.dumps({"access_token": access_token, "token_type": "bearer"}))
            res.headers['Content-Type'] = 'application/json'
            return res
            # return {"message": "Login successful"}
