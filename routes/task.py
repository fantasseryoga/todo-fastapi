from datetime import datetime
from typing import Annotated
from jose import jwt
from bson import ObjectId
from schemas.task import taskEntity, tasksEntity
from schemas.user import userEntity
from fastapi import APIRouter, HTTPException, Header, Depends, Response
from config.db import db
from models.task import Task
from models.search import TasksSearch
from models.taskUpdate import TaskUpdate
from utils.jwt import get_current_user
from traceback import print_exception
import configparser

config = configparser.ConfigParser()
config.read("settings/settings.ini")

task = APIRouter()


@task.post('/tasks-by-user/')
async def get_user_tasks(search: TasksSearch | None = TasksSearch, user: userEntity = Depends(get_current_user)):
    try:
        tasks = db["tasks"]
        
        if search:
            cursor = tasks.find({"userId": str(user["id"]), "title": {"$regex": search.title if search.title else ""}, "status": search.status if search.status else {"$ne": "deleted"}})
        else:
            cursor = tasks.find({"userId": str(user["id"])})


        tasks_db = []
        for document in await cursor.to_list(length=1000):
            tasks_db.append(document)
            
    except Exception:
        raise HTTPException(status_code=500, detail='Internal Server Error')

    return tasksEntity(tasks_db)


@task.put('/task')
async def update_task(task: TaskUpdate, user: userEntity = Depends(get_current_user)):
    try:
        tasks = db["tasks"]
        cursor = tasks.find({"_id": ObjectId(task.taskId), "userId": str(user["id"])})
        task_db = None
        
        for document in await cursor.to_list(length=1):
            task_db = document

        if task_db == None:
            raise HTTPException(status_code=404, detail='Task not found')
        
        updatedOn = datetime.now()
        tasks.find_one_and_update({"_id": ObjectId(task.taskId)}, {"$set": {"status": task.status.value, "updatedOn": updatedOn}})
        task_db["status"] = task.status.value
        task_db["updatedOn"] = updatedOn
        
    except Exception:
        raise HTTPException(status_code=500, detail='Internal Server Error')
    
    return taskEntity(task_db)


@task.post('/task')
async def create_task(task: Task, user: userEntity = Depends(get_current_user)):
    try:
        tasks = db["tasks"]
        
        task.userId = str(user["id"])

        task_status = task.status.value
        task = task.dict()

        task["status"] = task_status

    except Exception:
        raise HTTPException(status_code=500, detail='Internal Server Error')
    
    result = await tasks.insert_one(task)
    
    return {"message": "task created"}