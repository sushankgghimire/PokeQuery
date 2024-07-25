from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter()

@router.get("/pokemons", response_model=list[schemas.Pokemon])
async def read_pokemons(name: str = None, type: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pokemons = await crud.get_pokemons(db, name=name, type=type, skip=skip, limit=limit)
    return pokemons

@router.post("/pokemons", response_model=schemas.Pokemon)
async def create_pokemon(pokemon: schemas.PokemonCreate, db: Session = Depends(get_db)):
    db_pokemon = await crud.get_pokemon_by_name(db, name=pokemon.name)
    if db_pokemon:
        raise HTTPException(status_code=400, detail="Pokemon already registered")
    return await crud.create_pokemon(db=db, pokemon=pokemon)
