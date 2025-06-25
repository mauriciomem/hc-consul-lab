from datetime import datetime
from sqlalchemy import create_engine, select, text, Column, Integer, String
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool, QueuePool
from config.settings import Settings
from core.models import PetResponse, PetSchema
from typing import List, Generator, Optional
from core.logger import setup_logger
import time

logger = setup_logger()

logger.info('loading logger in {}'.format(__name__))

DATABASE_URL = Settings.SQLALCHEMY_DATABASE_URI

# Create engine with connection pooling and retry logic
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600,
    pool_pre_ping=True,  # This will test connections before using them
    connect_args={
        "connect_timeout": 10,
        "options": "-c statement_timeout=30000"  # 30 second statement timeout
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Pet(Base):
    __tablename__ = "pets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    species = Column(String, index=True)
    guardian = Column(String)
    age = Column(Integer)
    breed = Column(String, nullable=True)
    creation_date = Column(String, default=datetime.now().strftime("%y-%m-%d %H:%M"))

def get_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def check_db_connection() -> bool:
    """
    Check if database connection is available without raising exceptions
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            conn.close()
        return True
    except Exception as e:
        logger.error(f"Database connection check failed: {e}")
        return False

def is_alive() -> bool:
    """
    Legacy function for backward compatibility
    """
    return check_db_connection()

def ensure_tables_exist() -> bool:
    """
    Ensure database tables exist, with retry logic
    """
    max_retries = 3
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            Base.metadata.create_all(bind=engine)
            logger.info("Database tables verified/created successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to create tables (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                logger.error("Failed to create tables after all retries")
                return False
    return False

def get_all_pets(db: Session, species: str = None) -> Optional[List[PetResponse]]:
    """
    Get all pets with proper error handling
    """
    try:
        if species == "cat":
            statement = select(Pet).where(Pet.species == "cat")
        elif species == "dog":
            statement = select(Pet).where(Pet.species == "dog")
        else:
            statement = select(Pet)
        
        pets = db.scalars(statement).all()
        if not pets:
            return None
        return pets
    except Exception as e:
        logger.error(f"Failed to get all pets: {e}")
        db.rollback()
        raise

def new_pet(db: Session, pet: PetSchema) -> PetResponse:
    """
    Create a new pet with proper error handling
    """
    try:
        db_pet = Pet(
            name=pet.name, 
            species=pet.species, 
            age=pet.age, 
            breed=pet.breed, 
            guardian=pet.guardian, 
            creation_date=datetime.now().strftime("%y-%m-%d %H:%M")
        )
        db.add(db_pet)
        db.commit()
        db.refresh(db_pet)
        return db_pet
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create a new pet: {e}")
        raise

def del_pet(pet_id: int, db: Session) -> Optional[PetResponse]:
    """
    Delete a pet with proper error handling
    """
    try:
        statement = select(Pet).where(Pet.id == pet_id)
        pet = db.scalars(statement).first()
        if pet:
            db.delete(pet)
            db.commit()
            return pet
        else:
            return None
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to delete pet: {e}")
        raise

def upd_pet(pet_id: int, pet: PetSchema, db: Session) -> Optional[PetResponse]:
    """
    Update a pet with proper error handling
    """
    try:
        statement = select(Pet).where(Pet.id == pet_id)
        update = db.scalars(statement).first()
        if not update:
            return None
        
        update.name = pet.name
        update.species = pet.species
        update.guardian = pet.guardian
        update.age = pet.age
        update.breed = pet.breed
        
        db.commit()
        db.refresh(update)
        return update

    except Exception as e:
        db.rollback()
        logger.error(f"Failed to update pet: {e}")
        raise

def preload_pets_db() -> bool:
    """
    Preload sample pets into the database with better error handling
    """
    try:
        # First ensure tables exist
        if not ensure_tables_exist():
            logger.error("Cannot preload pets - tables don't exist")
            return False
            
        db = SessionLocal()
        try:
            # Check if we already have pets
            existing_pets = db.query(Pet).count()
            if existing_pets == 0:
                logger.info("No pets found, loading sample pets")
                pet1 = Pet(
                    name="Marti",
                    species="dog",
                    age=9,
                    breed="mixed",
                    guardian="Malu",
                    creation_date=datetime.now().strftime("%y-%m-%d %H:%M")
                )
                pet2 = Pet(
                    name="Boby",
                    species="dog",
                    age=5,
                    breed="Beagle",
                    guardian="Armon",
                    creation_date=datetime.now().strftime("%y-%m-%d %H:%M")
                )
                pet3 = Pet(
                    name="Hashi",
                    species="cat",
                    age=3,
                    breed="Bengal",
                    guardian="Mitchell",
                    creation_date=datetime.now().strftime("%y-%m-%d %H:%M")
                )
                db.add_all([pet1, pet2, pet3])
                db.commit()
                logger.info("Sample pets loaded successfully")
            else:
                logger.info(f"Database already contains {existing_pets} pets")
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to preload pets: {e}")
            return False
        finally:
            db.close()
    except Exception as e:
        logger.error(f"Failed to connect to database for preloading: {e}")
        return False