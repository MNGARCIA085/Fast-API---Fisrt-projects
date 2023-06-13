from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import exc
from database.configuration import get_db
from staff import models
from auth.models import User
from staff import schemas
import functools



# create new user (tmb. podría hacerlo que si no está inserte el usuario y sino sólo inserta el doctor)
# por ahora está separado (le voy a mostrar la lista de usuarios de staff y que ingrese el tipo)
# en realidad como debe ingresar la especialidad esto no es muy necesario
def post_doctor(user_id, db: Session = Depends(get_db)):
    db_item = models.Doctor(user_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item



def get_doctors(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
    ):
    """
    from sqlalchemy import join
    from sqlalchemy.sql import select
    j = students.join(addresses, students.c.id == addresses.c.st_id)
    stmt = select([students]).select_from(j)
    result = conn.execute(stmt)
    result.fetchall()
    """
    return db.query(models.Doctor).offset(skip).limit(limit).all()
    return db.query(models.Doctor).join(User).offset(skip).limit(limit).all()
    return list(db.query(models.Doctor).join(User,User.id == models.Doctor.user, isouter=True).offset(skip).limit(limit).all())
    #return db.query(models.Doctor).join(User).offset(skip).limit(limit).all()



def get_doctor_by_id(doctor_id:int,db: Session = Depends(get_db)):
    doc = db.query(models.Doctor).filter(models.Doctor.id==doctor_id).first()
    if doc:
        return doc
    raise HTTPException(status_code=404, detail="Doctor not found")



def delete_doctor(doctor_id,db: Session = Depends(get_db)):
    aux = db.query(models.Doctor).filter_by(id=sede_id).delete()
    if aux == 0:
        raise HTTPException(status_code=400, detail="Doctor with id %s not found" % doctor_id)
    else:
        db.commit()
    return {'Msg':"Doctor with id %s deleted" % doctor_id}
