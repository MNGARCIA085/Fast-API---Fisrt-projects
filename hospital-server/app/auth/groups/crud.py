from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import exc
from database.configuration import get_db
from .. import models,schemas




# create new group
def post_group(group: schemas.Groups, db: Session = Depends(get_db)):
    db_item = models.Groups(**group.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item



# return all groups
def get_groups(
            skip: int = 0, 
            limit: int = 100, 
            db: Session = Depends(get_db)):   
    return db.query(models.Groups).offset(skip).limit(limit).all()


# get group by id
def get_group_by_id(group_id, db: Session = Depends(get_db)):
    return db.query(models.Groups).filter(models.Groups.id == group_id).first()


# delete group
def delete_group(group_id,db: Session = Depends(get_db)):
    try:
        aux = db.query(models.Groups).filter_by(id=group_id).delete()
        if aux == 0:
            raise HTTPException(status_code=400, detail="Group with id %s not found" % group_id)
        else:
            db.commit()
        return {'Msg':"Group with id %s deleted" % group_id}
    except HTTPException as e:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server Error")
    return
