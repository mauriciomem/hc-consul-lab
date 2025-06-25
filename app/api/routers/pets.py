from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.orm import Session
from core.db import get_session, is_alive, get_all_pets, new_pet, del_pet, upd_pet
from core.models import PetSchema, PetResponse
from typing import List
from core.logger import setup_logger

logger = setup_logger()

logger.info('loading logger in {}'.format(__name__))

router = APIRouter()

@router.get("/health")
def health_check(request: Request) -> dict:

    logger.info(f"Health check")
    logger.debug(f"Request: {request}")

    if is_alive():
        database_status = "online"
    else:
        database_status = "offline"

    return {
        "api": "online",
        "database": database_status
    }

# GET all pets
@router.get("/pets", response_model=List[PetResponse])
def get_pets(db: Session = Depends(get_session)):
    
    logger.info(f"Getting all pets")

    pets_out = get_all_pets(db)
    if not pets_out:
        raise HTTPException(status_code=404, detail="No pets found")
    return pets_out

# POST a new pet
@router.post("/pets", response_model=PetResponse)
def create_pet(pet: PetSchema, db: Session = Depends(get_session)):

    logger.info(f"Creating new pet: {pet}")

    pet_out = new_pet(db, pet)
    return pet_out

# GET only cats
@router.get("/pets/cats", response_model=List[PetResponse])
def get_cats(db: Session = Depends(get_session)):
    
    logger.info(f"Getting all cats")

    cats_out = get_all_pets(db, species="cat")

    if not cats_out:
        raise HTTPException(status_code=404, detail="No cats found")
    return cats_out

# GET only dogs
@router.get("/pets/dogs", response_model=List[PetResponse])
def get_dogs(db: Session = Depends(get_session)):
    
    logger.info(f"Getting all dogs")

    dogs_out = get_all_pets(db, species="dog")

    if not dogs_out:
        raise HTTPException(status_code=404, detail="No dogs found")
    return dogs_out

# DELETE a pet
@router.delete("/pets/{pet_id}", response_model=PetResponse)
def delete_pet(pet_id: int, db: Session = Depends(get_session)):
    
    logger.info(f"Deleting pet")
    
    pet_out = del_pet(pet_id, db)
    if not pet_out:
        raise HTTPException(status_code=404, detail="No pet found")

    logger.info(f"Pet {pet_out.name} deleted")

    return pet_out

# UPDATE a pet
@router.put("/pets/{pet_id}", response_model=PetResponse)
def update_pet(pet_id: int, pet: PetSchema, db: Session = Depends(get_session)):

    logger.info(f"Updating pet")

    pet_out = upd_pet(pet_id, pet, db)
    if not pet_out:
        raise HTTPException(status_code=404, detail="No pet found")
    
    logger.info(f"Pet {pet_out.name} updated")

    return pet_out