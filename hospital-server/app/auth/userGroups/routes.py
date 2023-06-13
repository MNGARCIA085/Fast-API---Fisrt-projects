from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from database.configuration import get_db
from .. import models, schemas
from . import crud


router = APIRouter(
    prefix="/userAndGroups",
    responses={404: {"description": "Not found"}},
)


# agregar usuario y grupos a los que pertenece (le paso un usuario y el id de los grupos)
@router.post("/",status_code=201)
def create_user_and_groups(
                        user: schemas.User, 
                        groups: list[int], 
                        db: Session = Depends(get_db)):
    return crud.create_user_and_assign(user,groups,db)



# edit groups per user (tmb. sirve paa borrar todos los grupos si asi lo quiero)
@router.put("/{user_id}",status_code=201)
def edit_groups_per_user(
                        user_id, 
                        groups:schemas.listaFK, 
                        db: Session = Depends(get_db)):
    print('ruta',groups)
    return crud.edit_groups_per_user(user_id,groups,db)



#https://dassum.medium.com/building-rest-apis-using-fastapi-sqlalchemy-uvicorn-8a163ccf3aa1
#https://hackersandslackers.com/database-queries-sqlalchemy-orm/