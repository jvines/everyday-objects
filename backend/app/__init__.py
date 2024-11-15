from fastapi import FastAPI
from .database import engine, Base
from .database.utils import lifespan
from .routers import everyday


def create_app():
    Base.metadata.create_all(bind=engine)
    app = FastAPI(lifespan=lifespan)
    app.include_router(everyday.router)
    
    return app
