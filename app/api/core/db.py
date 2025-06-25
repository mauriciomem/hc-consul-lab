from datetime import datetime
from sqlalchemy import create_engine, select, text, Column, Integer, String
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config.settings import Settings
from core.models import PetResponse, PetSchema
from typing import List, Generator
from core.logger import setup_logger

logger = setup_logger()

logger.info('loading logger in {}'.format(__name__))

DATABASE_URL = Settings.SQLALCHEMY_DATABASE_URI

engine = create_engine(DATABASE_URL)

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

Base.metadata.create_all(bind=engine)

def get_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def is_alive() -> bool:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        logger.error("Database is not live")
        return False

def get_all_pets(db: Session, species: str = None) -> List[PetResponse] | None:
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
    except Exception:
        logger.error("Failed to get all pets")
        raise

def new_pet(db: Session, pet: Pet) -> PetResponse:
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
    except Exception:
        db.rollback()
        logger.error("Failed to create a new pet")
        raise

def del_pet(pet_id: int, db: Session) -> PetResponse | None:
    try:
        statement = select(Pet).where(Pet.id == pet_id)
        pet = db.scalars(statement).first()
        if pet:
            db.delete(pet)
            db.commit()
            return pet
        else:
            return None
    except Exception:
        db.rollback()
        logger.error("Failed to delete pet")
        raise

def upd_pet(pet_id: int, pet: PetSchema, db: Session) -> PetResponse | None:
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

    except Exception:
        db.rollback()
        logger.error("Failed to update pet")
        raise

def preload_pets_db() -> bool:
    try:
        db = SessionLocal()
        if db.query(Pet).count() == 0:
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
            db.close()
        return True
    except Exception:
        db.rollback()
        logger.error("Database is not live")
        return False