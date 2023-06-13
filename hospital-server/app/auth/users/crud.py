from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import exc
from database.configuration import get_db
from .. import models,schemas
import functools


# create new user
def post_user(user: schemas.User, db: Session = Depends(get_db)):
    db_item = models.User(**user.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# mapeo de nombres y claves; tmb. podría definir consultas del tipo FK
def mapeo():
    return {
        "name": models.User.name,
        "last_name": models.User.last_name,
        # groups
    }


def filter_user(data):
    queries = [models.User.id > 0]
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


def get_users(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        name: str | None = None,
        last_name: str | None = None,
):
    # filtrado
    query = filter_user(
        {
            'name': name,
            'last_name': last_name,
        })
    return list(db.query(models.User).filter(query).offset(skip).limit(limit))


# get user by id
def get_user_by_id(user_id, db: Session = Depends(get_db)):
    return db.query(models.User).filter(models.User.id == user_id).first()


# update user
def update_user(user_id: int, user: schemas.User, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        user_data = user.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return db_user
    else:
        raise HTTPException(status_code=400, detail="User with id %s not found" % user_id)


# delete an user
def delete_user(user_id,db: Session = Depends(get_db)):
    try:
        aux = db.query(models.User).filter_by(id=user_id).delete()
        if aux == 0:
            raise HTTPException(status_code=400, detail="User with id %s not found" % user_id)
        else:
            db.commit()
        return {'Msg':"User with id %s deleted" % user_id}
    except HTTPException as e:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Server Error")
    return