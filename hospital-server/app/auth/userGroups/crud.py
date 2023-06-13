from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import exc
from ..groups.crud import get_group_by_id
from database.configuration import get_db
from .. import models, schemas


# add an user and give him a list of groups by id """
def create_user_and_assign(
                user: schemas.User, 
                groups: list[int], 
                db: Session = Depends(get_db)):
    try:
        # valido que los grupos sean válidos
        db_user = models.User(**user.dict())
        db.add(db_user)
        db.flush()
        u = db_user.id
        for g in groups:
            aux = get_group_by_id(g,db)
            if aux:
                db_item = models.UserGroups(user_id=u,group_id=g)
                db.add(db_item)
        db.commit()
        db.refresh(db_user)
    #except exc.SQLAlchemyError:
    #    print(exc.SQLAlchemyError)
    except:
        pass # db.rollback()
    return {'User':db_user,'Groups':groups}




# edit the groups for an user
def edit_groups_per_user(u: int, groups:schemas.listaFK,db: Session = Depends(get_db)):
    # borro los viejos
    db.query(models.UserGroups).filter_by(user_id=u).delete()
    # inserto
    for g in groups.groups:
        db_userGroup = models.UserGroups(user_id=u,group_id=g)
        db.add(db_userGroup)
    db.commit()
    return {'User':u,'Groups':groups}



# ej delete: db.query(models.UserGroups).filter(models.UserGroups.group_id.in_(groups),models.UserGroups.user_id==u).delete()
