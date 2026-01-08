
from pydantic import BaseModel, ConfigDict
from datetime import date

class EmployeeCreate(BaseModel):
    name: str
    email: str
    role: str
    userrole:str
    date_joined: date


class EmployeeResponse(EmployeeCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
    
class EmployeeOut(BaseModel):
    id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
