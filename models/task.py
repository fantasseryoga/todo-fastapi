from pydantic import BaseModel, validator
from datetime import datetime
from enum import Enum
import pytz

utc=pytz.UTC

class Status(Enum):
    ACTIVE = "active"
    DONE = "done"
    FAILED = "failed"
    DELETED = "deleted"


class Task(BaseModel):
    title: str
    status: Status
    priority: int
    date: datetime
    createdOn: datetime = datetime.now()
    updatedOn: datetime = datetime.now()
    userId: str = None

    @validator('title')
    def title_lng_check(v: str):
        if len(v) > 20:
            raise ValueError('Title should contain a maximum of 100 characters')
        if len(v) < 2:
            raise ValueError('Title should contain a minimum of 2 characters')
        
        return v
    
    @validator('priority')
    def priority_range_check(v: int):
        if (1 <= v <= 5) == False:
            raise ValueError('Priority should be in 1-5 range')
        
        return v
        
    @validator('date')
    def date_check(v: datetime):
        if v.replace(tzinfo=utc) < datetime.now().replace(tzinfo=utc):
            raise ValueError('Date should be in future')
        
        return v