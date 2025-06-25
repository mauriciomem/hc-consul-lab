from fastapi import FastAPI
from routers import pets
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from core.db import preload_pets_db
from core.logger import setup_logger

logger = setup_logger()

logger.info('loading logger in {}'.format(__name__))

def preload_pets():
    logger.info("Preloading pets")
    preload_pets_db()

def create_app() -> FastAPI:

    @asynccontextmanager
    async def lifecycle(app: FastAPI):
        logger.info("Starting application")
        preload_pets()
        yield
        logger.info("Shutting down application")

    app = FastAPI(lifespan=lifecycle)
    app.include_router(pets.router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app

app = create_app()