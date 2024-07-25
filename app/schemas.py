from pydantic import BaseModel

# pydantic models to access the data
class PokemonBase(BaseModel):
    name: str
    image_url: str
    type: str

class PokemonCreate(PokemonBase):
    pass

class Pokemon(PokemonBase):
    id: int

    class Config:
        from_attributes = True
