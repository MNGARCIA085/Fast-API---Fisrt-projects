from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from database.configuration import get_db
from .. import schemas
from . import crud


router = APIRouter(
    prefix="/users",
    responses={404: {"description": "Not found"}},
)




# post a new user
@router.post("/",status_code=201,response_model=schemas.UserOut) 
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    return crud.post_user(user=user,db=db)


# get user
@router.get("/",response_model=list[schemas.UserOut])
def read_users(
                skip: int = 0, 
                limit: int = 100, 
                db: Session = Depends(get_db),
                name: str | None = None,
                last_name: str | None = None,
            ):
        return crud.get_users(
                skip=skip,
                limit=limit,
                last_name=last_name,
                name=name,
                db=db
            )


# get user by id
@router.get("/{user_id}",response_model=schemas.UserOut) #,
def read_user(user_id,db: Session = Depends(get_db)):
    return crud.get_user_by_id(user_id,db)


# Update an user
@router.put('/{user_id}',response_model=schemas.UserOut,status_code=201)
def update_user(user_id: int,user: schemas.User, db: Session = Depends(get_db)):
    return crud.update_user(user_id,user,db)


# Delete an user
@router.delete("/{user_id}") #, response_model=schemas.User
def delete_user(user_id,db: Session = Depends(get_db)):
    return crud.delete_user(user_id,db)