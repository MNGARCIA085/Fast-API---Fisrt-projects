from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import exc
from database.configuration import get_db
from staff import models,schemas
import functools




def post_especialidad(especialidad: schemas.Especialidad, db: Session = Depends(get_db)):
    db_item = models.Especialidad(**especialidad.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item



def get_especialidades(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
    ):
    return db.query(models.Especialidad).offset(skip).limit(limit).all()



def get_especialidad_by_id(especialidad_id:int,db: Session = Depends(get_db)):
    doc = db.query(models.Especialidad).filter(models.Especialidad.id==especialidad_id).first()
    if doc:
        return doc
    raise HTTPException(status_code=404, detail="Record not found")



def delete_espeacialidad(especialidad_id,db: Session = Depends(get_db)):
    aux = db.query(models.Especialidad).filter_by(id=sede_id).delete()
    if aux == 0:
        raise HTTPException(status_code=400, detail="Especialidad with id %s not found" % especialidad_id)
    else:
        db.commit()
    return {'Msg':"Record with id %s deleted" % especialidad_id}
