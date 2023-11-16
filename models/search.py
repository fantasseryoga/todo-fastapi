from pydantic import BaseModel

class TasksSearch(BaseModel):
    title: str = ""
    status: str = None