from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from database.configuration import get_db
from .. import schemas
from . import crud



router = APIRouter(
    prefix="/groups",
    responses={404: {"description": "Not found"}},
)




# create a new group
@router.post("/",status_code=201) #, response_model=schemas.User
def create_group(group: schemas.Groups, db: Session = Depends(get_db)):
    return crud.post_group(group,db)


# list of all groups
@router.get("/",response_model=list[schemas.GroupsOut])
def read_groups(
            skip: int = 0, 
            limit: int = 100, 
            db: Session = Depends(get_db),
        ):
        return crud.get_groups(skip,limit,db)


# get group by id
@router.get("/{group_id}",response_model=schemas.GroupsOut) #,
def read_user(group_id,db: Session = Depends(get_db)):
    return crud.get_group_by_id(group_id,db)



# Delete a group
@router.delete("/{group_id}") #, response_model=schemas.User
def delete_user(group_id,db: Session = Depends(get_db)):
    return crud.delete_group(group_id,db)