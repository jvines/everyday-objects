from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .database.utils import lifespan
from .routers import everyday


origins = [
    "http://localhost:5173",
    "http://localhost:5174"
]


def create_app():
    Base.metadata.create_all(bind=engine)
    app = FastAPI(lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )
    app.include_router(everyday.router)
    
    return app
