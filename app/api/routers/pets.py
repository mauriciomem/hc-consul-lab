from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from core.db import get_session, is_alive, get_all_pets, new_pet, del_pet, upd_pet
from core.models import PetSchema, PetResponse
from core.db_status import db_status
from typing import List
from core.logger import setup_logger
import asyncio

logger = setup_logger()

logger.info('loading logger in {}'.format(__name__))

router = APIRouter()

class DatabaseConnectionError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=503,
            detail="Database service is currently unavailable. Please try again later."
        )

def handle_db_errors(func):
    """
    Decorator to handle database errors gracefully
    """
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
        except OperationalError as e:
            logger.error(f"Database operational error: {e}")
            raise DatabaseConnectionError()
        except SQLAlchemyError as e:
            logger.error(f"Database error: {e}")
            raise HTTPException(status_code=500, detail="Internal database error")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
    return wrapper

@router.get("/health")
def health_check(request: Request) -> dict:
    """
    Health check endpoint that reports API and database status
    """
    logger.info(f"Health check")
    logger.debug(f"Request: {request}")

    database_status = "online" if is_alive() else "offline"

    response = {
        "api": "online",
        "database": database_status
    }
    
    # Return 200 even if database is offline (API is still running)
    # You could change this to return 503 if you want the health check
    # to fail when database is unavailable
    return response

@router.get("/db-status")
async def get_db_status() -> dict:
    """
    Get detailed database connection status with fresh check
    """
    logger.info("Database status check requested")
    
    # Perform a fresh check
    try:
        from core.db import check_db_connection
        is_connected = await asyncio.to_thread(check_db_connection)
        db_status.update_status(is_connected)
    except Exception as e:
        logger.error(f"Error checking database status: {e}")
        db_status.update_status(False)
    
    return db_status.get_status()

# GET all pets
@router.get("/pets", response_model=List[PetResponse])
def get_pets(db: Session = Depends(get_session)):
    """
    Get all pets with database error handling
    """
    logger.info(f"Getting all pets")
    
    try:
        pets_out = get_all_pets(db)
        if not pets_out:
            raise HTTPException(status_code=404, detail="No pets found")
        return pets_out
    except OperationalError as e:
        logger.error(f"Database connection error: {e}")
        raise DatabaseConnectionError()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error getting pets: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# POST a new pet
@router.post("/pets", response_model=PetResponse)
def create_pet(pet: PetSchema, db: Session = Depends(get_session)):
    """
    Create a new pet with database error handling
    """
    logger.info(f"Creating new pet: {pet}")
    
    try:
        pet_out = new_pet(db, pet)
        return pet_out
    except OperationalError as e:
        logger.error(f"Database connection error: {e}")
        raise DatabaseConnectionError()
    except Exception as e:
        logger.error(f"Unexpected error creating pet: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# GET only cats
@router.get("/pets/cats", response_model=List[PetResponse])
def get_cats(db: Session = Depends(get_session)):
    """
    Get all cats with database error handling
    """
    logger.info(f"Getting all cats")
    
    try:
        cats_out = get_all_pets(db, species="cat")
        if not cats_out:
            raise HTTPException(status_code=404, detail="No cats found")
        return cats_out
    except OperationalError as e:
        logger.error(f"Database connection error: {e}")
        raise DatabaseConnectionError()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error getting cats: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# GET only dogs
@router.get("/pets/dogs", response_model=List[PetResponse])
def get_dogs(db: Session = Depends(get_session)):
    """
    Get all dogs with database error handling
    """
    logger.info(f"Getting all dogs")
    
    try:
        dogs_out = get_all_pets(db, species="dog")
        if not dogs_out:
            raise HTTPException(status_code=404, detail="No dogs found")
        return dogs_out
    except OperationalError as e:
        logger.error(f"Database connection error: {e}")
        raise DatabaseConnectionError()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error getting dogs: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# DELETE a pet
@router.delete("/pets/{pet_id}", response_model=PetResponse)
def delete_pet(pet_id: int, db: Session = Depends(get_session)):
    """
    Delete a pet with database error handling
    """
    logger.info(f"Deleting pet")
    
    try:
        pet_out = del_pet(pet_id, db)
        if not pet_out:
            raise HTTPException(status_code=404, detail="No pet found")
        
        logger.info(f"Pet {pet_out.name} deleted")
        return pet_out
    except OperationalError as e:
        logger.error(f"Database connection error: {e}")
        raise DatabaseConnectionError()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error deleting pet: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# UPDATE a pet
@router.put("/pets/{pet_id}", response_model=PetResponse)
def update_pet(pet_id: int, pet: PetSchema, db: Session = Depends(get_session)):
    """
    Update a pet with database error handling
    """
    logger.info(f"Updating pet")
    
    try:
        pet_out = upd_pet(pet_id, pet, db)
        if not pet_out:
            raise HTTPException(status_code=404, detail="No pet found")
        
        logger.info(f"Pet {pet_out.name} updated")
        return pet_out
    except OperationalError as e:
        logger.error(f"Database connection error: {e}")
        raise DatabaseConnectionError()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error updating pet: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")