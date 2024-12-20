from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database.utils import lifespan
from .routers import everyday


origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
]


def create_app():
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
