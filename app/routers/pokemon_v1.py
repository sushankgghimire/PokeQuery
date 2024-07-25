from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter()

@router.get("/pokemons", response_model=list[schemas.Pokemon])
async def read_pokemons(
    name: str = None,
    type: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of Pokémon from the database.

    - **name**: Filter Pokémon by name (optional).
    - **type**: Filter Pokémon by type (optional).
    - **skip**: Number of Pokémon to skip (pagination) (default: 0).
    - **limit**: Number of Pokémon to return (pagination) (default: 100).

    Returns a list of Pokémon objects matching the query parameters.
    """
    pokemons = await crud.get_pokemons(db, name=name, type=type, skip=skip, limit=limit)
    return pokemons

@router.post("/pokemons", response_model=schemas.Pokemon)
async def create_pokemon(
    pokemon: schemas.PokemonCreate,
    db: Session = Depends(get_db)
):
    """
    Add a new Pokémon to the database.

    - **pokemon**: Pokémon object containing the name, image URL, and type of the Pokémon.

    Checks if the Pokémon already exists by name. If it does, a 400 HTTP exception is raised. Otherwise, creates and returns the new Pokémon.
    """
    db_pokemon = await crud.get_pokemon_by_name(db, name=pokemon.name)
    if db_pokemon:
        raise HTTPException(status_code=400, detail="Pokemon already registered")
    return await crud.create_pokemon(db=db, pokemon=pokemon)
