from fastapi import Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database.configuration import get_db
from . import models
from . import schemas
import functools

""" 1. GET """


# mapeo de nombres y claves; tmb. podría definir consultas del tipo FK
def mapeo():
    return {
        "tipo": models.Sede.tipo,
        "direccion": models.Sede.direccion,
        "nombre": models.Sede.nombre,
    }


def filter_department(data):
    queries = [models.Sede.id > 0]
    campos = mapeo()
    for clave, valor in data.items():
        if valor:
            if isinstance(valor, str):
                queries.append(campos[clave] == valor)
            elif isinstance(valor, list):
                queries_aux = []
                for v in valor:
                    queries_aux.append(campos[clave] == v)
                query_aux = functools.reduce(lambda a, b: a | b, queries_aux)
                queries.append(query_aux)
    query = functools.reduce(lambda a, b: (a & b), queries)
    return query


#
def get_departments(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        tipo: str | None = None,
        direccion: str | None = None,
        nombre: list[str] | None = Query(default=None),
):
    # filtrado
    query = filter_department(
        {
            'tipo': tipo,
            'direccion': direccion,
            'nombre': nombre
        })
    return list(db.query(models.Sede).filter(query).offset(skip).limit(limit))


""" 2. POST """


def post_department(sede: schemas.Sede, db: Session = Depends(get_db)):
    db_item = models.Sede(**sede.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item




""" 3. GET by id """
def get_dept_by_id(sede_id:int,db: Session = Depends(get_db)):
    sede = db.query(models.Sede).filter(models.Sede.id==sede_id).first()
    if sede:
        return sede
    raise HTTPException(status_code=404, detail="Department not found")




""" 4. UPDATE """
#https://stackoverflow.com/questions/63143731/update-sqlalchemy-orm-existing-model-from-posted-pydantic-model-in-fastapi

def update_department(sede_id: int, sede: schemas.Sede, db: Session = Depends(get_db)):
    db_sede = db.query(models.Sede).filter(models.Sede.id == sede_id).first()
    if db_sede:
        for var, value in vars(sede).items():
            setattr(db_sede, var, value) if value else None
        db.add(db_sede)
        db.commit()
        db.refresh(db_sede)
        return db_sede
    else:
        raise HTTPException(status_code=400, detail="Department with id %s not found" % sede_id)



""" 5. DELETE """
def delete_department(sede_id,db: Session = Depends(get_db)):
    try:
        aux = db.query(models.Sede).filter_by(id=sede_id).delete()
        if aux == 0:
            raise HTTPException(status_code=400, detail="Department with id %s not found" % sede_id)
        else:
            db.commit()
        return {'Msg':"Department with id %s deleted" % sede_id}
    except HTTPException as e:
        raise
    except Exception as e:
        #print(e); esto no va para el usuario sino para mi login
        raise HTTPException(status_code=500, detail="Server Error")
    return
