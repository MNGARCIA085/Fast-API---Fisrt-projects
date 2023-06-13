from typing import List
from fastapi import APIRouter,status,Body, Request, HTTPException,Response
from fastapi.encoders import jsonable_encoder
from .models import User,UserUpdate
from .security import get_password_hash

router = APIRouter(
    prefix="/users",
    responses={404: {"description": "Not found"}},
    tags=['users'],
)

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=User)
def create_user(request: Request, user: User = Body(...)):
    # que no exista ya
    if (request.app.database["users"].find_one({"username": user.username})) is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Username already taken")
    # ingreso
    user = jsonable_encoder(user)
    # hash de la contraseña
    hash_password = get_password_hash(user['password'])
    user['password'] = hash_password
    new_user = request.app.database["users"].insert_one(user)
    created_user = request.app.database["users"].find_one(
        {"_id": new_user.inserted_id}
    )
    return created_user



@router.get("/",response_model=List[User])
def list_users(request: Request):
   return list(request.app.database['users'].find(limit=100))


@router.get("/{id}",response_model=User)
def find_user(id: str, request: Request):
    if (user := request.app.database["users"].find_one({"_id": id})) is not None:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")


@router.put("/{id}", response_model=User)
def update_user(id: str, request: Request, user: UserUpdate = Body(...)):
    user = {k: v for k, v in user.dict().items() if v is not None}

    if len(user) >= 1:
        update_result = request.app.database["users"].update_one(
            {"_id": id}, {"$set": user}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")

    if (
        existing_movie := request.app.database["users"].find_one({"_id": id})
    ) is not None:
        return existing_movie

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")


@router.delete("/{id}", response_description="Delete a user")
def delete_user(id: str, request: Request, response: Response):
    delete_result = request.app.database["users"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")











