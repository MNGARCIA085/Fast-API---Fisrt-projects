from fastapi import APIRouter
from .users import routes as user_routes
from .groups import routes as group_routes
from .userGroups import routes as user_group_routes



router = APIRouter(
    prefix="/auth",
    responses={404: {"description": "Not found"}},
)



router.include_router(user_routes.router,tags=['users'])
router.include_router(group_routes.router,tags=['groups'])
router.include_router(user_group_routes.router,tags=['user_and_groups'])




