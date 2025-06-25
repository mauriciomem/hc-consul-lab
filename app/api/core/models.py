from pydantic import BaseModel, Field
from uuid import uuid4

class PetSchema(BaseModel):
    name: str = Field(example="Marti")
    species: str = Field(example="dog")
    age: int = Field(example=9)
    breed: str | None = None
    guardian: str = Field(example="Mitchell")

class PetResponse(PetSchema):
    id: int
    creation_date: str | None = None
    class Config:
        orm_mode = True