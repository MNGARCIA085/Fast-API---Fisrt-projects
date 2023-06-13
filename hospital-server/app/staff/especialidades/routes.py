from fastapi import APIRouter,Depends,HTTPException,Query
from sqlalchemy.orm import Session
from database.configuration import get_db
from . import crud
import functools
from staff import schemas


router = APIRouter(
    prefix="/especialidades",
    responses={404: {"description": "Not found"}},
)




@router.get("/",response_model=list[schemas.EspecialidadOut])
def read_especialidad(
                skip: int = 0, 
                limit: int = 100, 
                db: Session = Depends(get_db),
            ):
        return crud.get_especialidades(
                skip=skip,
                limit=limit,
                db=db
            )

# post
@router.post("/",status_code=201) #, response_model=schemas.User
def create_especialidad(especialidad: schemas.Especialidad, db: Session = Depends(get_db)):
    crud.post_especialidad(especialidad=especialidad,db=db)


# Get by id
@router.get("/{especialidad_id}",status_code=200,response_model=schemas.EspecialidadOut)
def get_especialidad_by_id(especialidad_id:int,db: Session = Depends(get_db)):
    return crud.get_especialidad_by_id(especialidad_id,db)


# Delete by id
@router.delete("/{especialidad_id}",status_code=200) #, response_model=schemas.SedeOut
def delete_especialidad(especialidad_id:int,db: Session = Depends(get_db)):
    return crud.delete_especialidad(especialidad_id,db)
