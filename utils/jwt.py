from datetime import datetime, timedelta
from typing import Union, Any, Annotated
from jose import jwt
from pydantic import ValidationError
from schemas.user import userEntity
from config.db import db
from fastapi import Depends, HTTPException, Header
from fastapi.security import OAuth2PasswordBearer
import configparser

config = configparser.ConfigParser()
config.read("settings/settings.ini")


reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)

config = configparser.ConfigParser()
config.read("settings/settings.ini")

def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=int(config["JWT"]["ACCESS_TOKEN_EXPIRE_MINUTES"]))
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, config["JWT"]["JWT_SECRET_KEY"], config["JWT"]["ALGORITHM"])
    return encoded_jwt

def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=int(config["JWT"]["REFRESH_TOKEN_EXPIRE_MINUTES"]))
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, config["JWT"]["JWT_REFRESH_SECRET_KEY"], config["JWT"]["ALGORITHM"])
    return encoded_jwt


async def get_current_user(token: Annotated[str | None, Header()] = None) -> userEntity:
    try:
        payload = jwt.decode(
            token, config["JWT"]["JWT_SECRET_KEY"], algorithms=[config["JWT"]["ALGORITHM"]]
        )

        
        if datetime.fromtimestamp(payload["exp"]) < datetime.now():
            raise HTTPException(
                status_code = 401,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    users = db["users"]
    cursor = users.find({"name": payload["sub"]}, limit=1)
    user = None
    for document in await cursor.to_list(length=1):
        user = document
    
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    
    return userEntity(user)
