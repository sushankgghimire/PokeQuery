from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app import models, schemas

async def get_pokemons(
    db: Session,
    name: str = None,
    type: str = None,
    skip: int = 0,
    limit: int = 100
):
    """
    Retrieve a list of Pokémon from the database with optional filters.

    - **db**: The database session object.
    - **name**: Filter Pokémon by name (optional).
    - **type**: Filter Pokémon by type (optional).
    - **skip**: Number of Pokémon to skip (pagination) (default: 0).
    - **limit**: Number of Pokémon to return (pagination) (default: 100).

    Returns a list of Pokémon objects that match the provided filters.

    If both `name` and `type` are provided, the query will filter Pokémon
    by both criteria. If only one of them is provided, the query will
    filter by that criterion. If neither is provided, it returns all
    Pokémon with pagination applied.
    """
    query = select(models.Pokemon).offset(skip).limit(limit)

    if name and type:
        query = query.filter(
            and_(
                models.Pokemon.name.ilike(f"%{name}%"),
                models.Pokemon.type.ilike(f"%{type}%")
            )
        )
    elif name:
        query = query.filter(models.Pokemon.name.ilike(f"%{name}%"))
    elif type:
        query = query.filter(models.Pokemon.type.ilike(f"%{type}%"))

    result = await db.execute(query)
    return result.scalars().all()

async def get_pokemon_by_name(db: Session, name: str):
    """
    Retrieve a single Pokémon by its name.

    - **db**: The database session object.
    - **name**: The name of the Pokémon to retrieve.

    Returns a Pokémon object if found, otherwise returns None.

    This function performs a query to find a Pokémon with the exact name
    provided. It returns the first match found or None if no match is
    found.
    """
    result = await db.execute(select(models.Pokemon).filter(models.Pokemon.name == name))
    return result.scalars().first()

async def create_pokemon(db: Session, pokemon: schemas.PokemonCreate):
    """
    Add a new Pokémon to the database.

    - **db**: The database session object.
    - **pokemon**: Pokémon data to be added to the database, provided as a
      `schemas.PokemonCreate` object.

    Returns the created Pokémon object.

    This function creates a new Pokémon entry in the database with the
    provided data. It commits the transaction and refreshes the Pokémon
    object to include any auto-generated fields such as ID.
    """
    db_pokemon = models.Pokemon(**pokemon.dict())
    db.add(db_pokemon)
    await db.commit()
    await db.refresh(db_pokemon)
    return db_pokemon
