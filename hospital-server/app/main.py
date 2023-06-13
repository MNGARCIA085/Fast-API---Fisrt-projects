from fastapi import FastAPI,APIRouter
from auth import routes as auth_routes
from departments import routes as dep_routes
from staff import routes as staff_routes
from config import settings


#

# creo las tablas
"""
from database.configuration import engine
from auth import models
models.Base.metadata.create_all(bind=engine)
"""


app = FastAPI()



# rutas
router = APIRouter()

app.include_router(auth_routes.router)
app.include_router(dep_routes.router,tags=['departments'])
app.include_router(staff_routes.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}



#print(settings)
# DB---> settings.DB_USER


@app.get("/info")
async def info():
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
    }




# with docker
#https://www.patrick-muehlbauer.com/articles/fastapi-with-sqlalchemy


# createdb with sqlalchemy
#https://stackoverflow.com/questions/6506578/how-to-create-a-new-database-using-sqlalchemy