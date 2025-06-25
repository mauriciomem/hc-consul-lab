from fastapi import FastAPI
from routers import pets
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from core.db import preload_pets_db, check_db_connection
from core.logger import setup_logger
from core.db_status import db_status
import asyncio
from typing import Optional

logger = setup_logger()

logger.info('loading logger in {}'.format(__name__))

async def monitor_database_connection(interval: int = 30):
    """
    Background task to monitor database connection every 'interval' seconds
    """
    # Perform initial check immediately
    try:
        logger.info("Performing initial database connection check")
        is_connected = await asyncio.to_thread(check_db_connection)
        db_status.update_status(is_connected)
        
        if not is_connected:
            logger.error("Initial check: Database connection unavailable")
        else:
            logger.info("Initial check: Database connection is healthy")
    except Exception as e:
        logger.error(f"Error during initial database connection check: {e}")
        db_status.update_status(False)
    
    # Continue with regular monitoring
    while True:
        await asyncio.sleep(interval)
        
        try:
            is_connected = await asyncio.to_thread(check_db_connection)
            db_status.update_status(is_connected)
            
            if not is_connected:
                logger.error("Database connection lost or unavailable")
            else:
                logger.debug("Database connection is healthy")
                
        except Exception as e:
            logger.error(f"Error checking database connection: {e}")
            db_status.update_status(False)

async def try_preload_pets(max_retries: int = 5, retry_delay: int = 5):
    """
    Try to preload pets with retry logic
    """
    for attempt in range(max_retries):
        try:
            logger.info(f"Attempting to preload pets (attempt {attempt + 1}/{max_retries})")
            success = await asyncio.to_thread(preload_pets_db)
            if success:
                logger.info("Successfully preloaded pets")
                return True
        except Exception as e:
            logger.warning(f"Failed to preload pets: {e}")
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
            else:
                logger.error("Max retries reached. Starting without preloaded pets.")
    return False

def create_app() -> FastAPI:

    @asynccontextmanager
    async def lifecycle(app: FastAPI):
        logger.info("Starting application")
        
        # Start database monitoring task
        monitor_task = asyncio.create_task(monitor_database_connection(interval=30))
        
        # Try to preload pets with retry logic
        await try_preload_pets()
        
        yield
        
        # Cancel monitoring task on shutdown
        monitor_task.cancel()
        try:
            await monitor_task
        except asyncio.CancelledError:
            pass
            
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