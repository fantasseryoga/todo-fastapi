from pydantic import BaseModel
from enum import Enum

class Status(Enum):
    ACTIVE = "active"
    DONE = "done"
    FAILED = "failed"
    DELETED = "deleted"


class TaskUpdate(BaseModel):
    taskId: str
    status: Status