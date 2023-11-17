from schemas.user import userEntity, usersEntity
from fastapi import APIRouter, HTTPException
from config.db import db
from models.user import User
import configparser
from utils.jwt import create_access_token, create_refresh_token
from utils.hash import Hasher

config = configparser.ConfigParser()
config.read("settings/settings.ini")

user = APIRouter()


@user.post('/log')
async def login_user(user: User):
    users = db["users"]
    cursor = users.find({"name": user.name}, limit=1)
    user_db = None
    for document in await cursor.to_list(length=1):
        user_db = document

    if user_db == None:
        raise HTTPException(status_code=400, detail='Invalid credentials')

    hasher = Hasher()
    valid_password = hasher.verify_password(user.password, user_db["password"])

    if valid_password == False:
        raise HTTPException(status_code=400, detail='Invalid credentials')
    
    return {
        "access_token": create_access_token(user_db['name']),
        "refresh_token": create_refresh_token(user_db['name']),
        "user": userEntity(user_db)
    }


@user.post('/reg')
async def create_user(user: User):
    users = db["users"]
    
    exists = await users.count_documents({"name": user.name}, limit = 1)
    if exists:
        raise HTTPException(status_code=400, detail='This username is already taken')
    
    hasher = Hasher()
    user.password = hasher.get_password_hash(user.password)
    user = user.dict()
    
    result = await users.insert_one(user)
    return {"message": "User created successfully "}
