from pydantic import BaseModel, validator
from datetime import datetime


class User(BaseModel):
    name: str
    password: str
    createdOn: datetime = datetime.now()

    @validator('name')
    def name_lng_check(v: str):
        if len(v) > 20:
            raise ValueError('Username should contain a maximum of 20 characters')
        if len(v) < 2:
            raise ValueError('Username should contain a minimum of 2 characters')
        
        return v
    
    @validator('password')
    def password_lng_check(v: str):
        if len(v) > 20:
            raise ValueError('Password should contain a maximum of 20 characters')
        if len(v) < 8:
            raise ValueError('Password should contain a minimum of 8 characters')
        
        return v
    
    @validator('password')
    def password_digits_check(v: str):
        if any(char.isdigit() for char in v) != True:
            raise ValueError('Password should contain at least 1 number')
        
        return v
    
    @validator('password')
    def password_capital_check(v: str):
        if any(char.isupper() for char in v) != True:
            raise ValueError('Password should contain at least 1 capital letter')
        
        return v
