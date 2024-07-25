from sqlalchemy.future import select
from sqlalchemy.orm import Session
from app import models, schemas

async def get_pokemons(db: Session, name: str = None, type: str = None, skip: int = 0, limit: int = 100):
    query = select(models.Pokemon).offset(skip).limit(limit)

    if name and type:
        query = query.filter(and_(models.Pokemon.name.ilike(f"%{name}%"), models.Pokemon.type.ilike(f"%{type}%")))
    elif name:
        query = query.filter(models.Pokemon.name.ilike(f"%{name}%"))
    elif type:
        query = query.filter(models.Pokemon.type.ilike(f"%{type}%"))

    result = await db.execute(query)
    return result.scalars().all()

async def get_pokemon_by_name(db: Session, name: str):
    result = await db.execute(select(models.Pokemon).filter(models.Pokemon.name == name))
    return result.scalars().first()

async def create_pokemon(db: Session, pokemon: schemas.PokemonCreate):
    db_pokemon = models.Pokemon(**pokemon.dict())
    db.add(db_pokemon)
    await db.commit()
    await db.refresh(db_pokemon)
    return db_pokemon
