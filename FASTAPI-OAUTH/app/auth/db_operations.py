from .utils import get_password_hash,verify_password
from databases.config import get_db
from . import schemas,models
from sqlalchemy.orm import Session
from fastapi import Depends


# get an user (returns a dict)
def get_user(db: Session, username: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user:
        #return schemas.UserInDB(**user.__dict__)
        return user
    else:
        return False


# authnticate user
def authenticate_user(username: str, password: str, db: Session):
    user = get_user(db,username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# create user
def create_user(user: schemas.UserRegister, db: Session = Depends(get_db)):
    hash_password = get_password_hash(user.password)
    db_user = models.User(email=user.email,
                          full_name=user.full_name,
                          hashed_password=hash_password,
                          username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user







