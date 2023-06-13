import uuid
from pydantic import BaseModel, Field

class User(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    username: str = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    password: str = Field(...)
    
    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "username": "mgarcia",
                "first_name":"marcos",
                "last_name":"garcía",
                "password":"1234"
            }
        }


class UserUpdate(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    password: str = Field(...)
    
    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "first_name":"marcos",
                "last_name":"garcía",
                "password":"1234"
            }
        }