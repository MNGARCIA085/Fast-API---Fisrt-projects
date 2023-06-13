from pydantic import BaseModel
from typing import List, Union, Optional
from auth.schemas import User

""" Base models """

class Especialidad(BaseModel):
    descripcion: str

    class Config:
        orm_mode = True


# model
class Doctor(BaseModel):
    user: User

    class Config:
        orm_mode = True


# response models

class EspecialidadOut(Especialidad):
    id:int
    doctor: List[Doctor]

    class Config:
        orm_mode = True


class DoctorOut(BaseModel):
    id:int
    user:Optional[User]
    especialidad: List[Especialidad]

    class Config:
        orm_mode = True



