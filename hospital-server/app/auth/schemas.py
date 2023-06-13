from pydantic import BaseModel
from typing import List, Union, Optional



class User(BaseModel):
    #id: int
    name: str
    last_name:Optional[str]

    class Config:
        orm_mode = True


class Groups(BaseModel):
    #id: int
    name: str

    class Config:
        orm_mode = True


# response models
class UserOut(User):
    id:int
    groups: Optional[List[Groups]]


class GroupsOut(Groups):
    id:int
    users: List[User]



# para pasar una lista de grupos (quizás le podría incluir un id)
class listaFK(BaseModel):
    groups:List[int]

