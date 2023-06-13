from fastapi import APIRouter,Depends,HTTPException,Query
from sqlalchemy.orm import Session
from database.configuration import get_db
from . import crud
import functools
from staff import schemas


router = APIRouter(
    prefix="/doctorAndSpecialties",
    responses={404: {"description": "Not found"}},
)


@router.post("/",status_code=201)
def create_doctor_and_specialties(
                        user_id: int, 
                        specialties: list[int], 
                        db: Session = Depends(get_db)):
    return crud.create_doctor_and_assign(user_id,specialties,db)




# delete groups per user
@router.delete("/")
def delete_specialties_per_doctor(
                        doctor_id: int, 
                        specialties: list[int], 
                        db: Session = Depends(get_db)):
    return crud.delete_specialties_per_doctor(doctor_id,specialties,db)



# edit groups per user
@router.put("/")
def edit_specialties_per_doctor(
                        doctor_id: int, 
                        specialties: list[int], 
                        db: Session = Depends(get_db)):
    return crud.edit_groups_per_user(doctor_id,specialties,db)