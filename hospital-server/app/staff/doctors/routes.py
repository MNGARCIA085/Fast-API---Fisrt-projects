from fastapi import APIRouter,Depends,HTTPException,Query
from sqlalchemy.orm import Session
from database.configuration import get_db
from . import crud
import functools
from staff import schemas


router = APIRouter(
    prefix="/doctors",
    responses={404: {"description": "Not found"}},
)




@router.get("/",response_model=list[schemas.DoctorOut]) #,response_model=list[schemas.DoctorOut]
def read_doctors(
                skip: int = 0, 
                limit: int = 100, 
                db: Session = Depends(get_db),
            ):
        return crud.get_doctors(
                skip=skip,
                limit=limit,
                db=db
            )

# post a new doctor
@router.post("/",status_code=201) #, response_model=schemas.User
def create_doctor(user_id: int, db: Session = Depends(get_db)):
    crud.post_doctor(user_id=user_id,db=db)


# Get by id
@router.get("/{doctor_id}",status_code=200,response_model=schemas.DoctorOut)
def get_doctor_by_id(doctor_id:int,db: Session = Depends(get_db)):
    return crud.get_doctor_by_id(doctor_id,db)


# Delete by id
@router.delete("/{doctor_id}",status_code=200) #, response_model=schemas.SedeOut
def delete_doctor(doctor_id:int,db: Session = Depends(get_db)):
    return crud.delete_doctor(doctor_id,db)
