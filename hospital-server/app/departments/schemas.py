from pydantic import BaseModel
from typing import List, Union, Optional



class Sede(BaseModel):
    #id: int
    nombre: str
    tipo:str
    direccion:str

    class Config:
        orm_mode = True


# response models
class SedeOut(Sede):
    id:int


