from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database.configuration import get_db
from staff.especialidades.crud import get_especialidad_by_id
import functools



# create a doctor and give him a list of specialties"""
def create_doctor_and_assign(
                user_id: int, 
                specialties: list[int], 
                db: Session = Depends(get_db)):
    try:
        db_doctor = models.Doctor(user_id=user_id)
        db.add(db_doctor)
        db.flush()
        d = db_doctor.id
        for s in specialties:
            aux = get_especialidad_by_id(s,db)
            if aux:
                db_item = models.DoctorEspecialidades(doctor_id=d,especialidad_id=s)
                db.add(db_item)
        db.commit()
    except Exception as e:
        print(e)
    return {'Msg':'Ok'}



# edit the specialties for a doctor
def edit_specialties_per_doctor(d: int, specialties:list[int],db: Session = Depends(get_db)):
    # borro los viejos
    db.query(models.DoctorEspecialidades).filter_by(doctor_id=d).delete()
    # inserto
    for s in specialties:
        db_doctorEspecialidad = models.DoctorEspecialidades(doctor_id=u,especialidad_id=g)
        db.add(db_userGroup)
    db.commit()
    return {'Msg':"Operation succeed"} 


# delete some specialties for a doctor
def delete_specialties_per_doctor(d: int, specialties:list[int],db: Session = Depends(get_db)):
    db.query(models.DoctorEspecialidades).filter(models.DoctorEspecialidades.especialidad_id.in_(specialties),models.DoctorEspecialidades.doctor_id==d).delete()
    db.commit()
    return {'Msg':"Operation succeed"}