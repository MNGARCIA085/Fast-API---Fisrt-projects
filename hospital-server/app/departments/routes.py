from fastapi import APIRouter,Depends,Query
from sqlalchemy.orm import Session
from database.configuration import get_db
from . import models
from . import schemas
from . import crud




router = APIRouter(
    prefix="/departments",
    responses={404: {"description": "Not found"}},
)



# Get
@router.get("/locations/",response_model=list[schemas.SedeOut])
def read_departments(
                skip: int = 0, 
                limit: int = 100, 
                db: Session = Depends(get_db),
                tipo: str | None = None,
                direccion: str | None = None,
                nombre: list[str] | None = Query(default=None),
            ):
        return crud.get_departments(
        		skip=skip,
        		limit=limit,
        		tipo=tipo,
        		direccion=direccion,
        		nombre=nombre,
        		db=db
        	)


# Post
@router.post("/locations/",status_code=201) #, response_model=schemas.SedeOut
def create_department(sede: schemas.Sede, db: Session = Depends(get_db)):
	return crud.post_department(sede=sede,db=db)



# Get by id
@router.get("/locations/{dept_id}",status_code=200) #, response_model=schemas.SedeOut
def get_department_by_id(dept_id:int,db: Session = Depends(get_db)):
	return crud.get_dept_by_id(dept_id,db)



# Update a dept
@router.put('/locations/{dept_id}',status_code=201)
def update_department(dept_id: int,sede:schemas.Sede ,db: Session = Depends(get_db)):
	return crud.update_department(dept_id,sede,db)


# Delete by id
@router.delete("/locations/{dept_id}",status_code=200) #, response_model=schemas.SedeOut
def delete_department(dept_id:int,db: Session = Depends(get_db)):
	return crud.delete_department(dept_id,db)





