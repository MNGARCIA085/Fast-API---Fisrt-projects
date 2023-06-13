from fastapi import FastAPI
from pymongo import MongoClient
from settings import settings
from movies import routes as movies_routes
from users import routes as user_routes


app = FastAPI()


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(settings.DB_URI)
    app.database = app.mongodb_client[settings.DB_NAME]

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
    


app.include_router(user_routes.router)


app.include_router(movies_routes.router)




















