from fastapi import FastAPI
from app.routers import pokemon_v1
import aiohttp
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import engine, Base, SessionLocal
from app.models import Pokemon
from app.schemas import PokemonCreate
from app.crud import create_pokemon, get_pokemons, get_pokemon_by_name

app = FastAPI()

# Include the Pokémon router with versioning in the FastAPI application
app.include_router(pokemon_v1.router, prefix="/api/v1")

async def fetch_and_store_pokemons():
    """
    Fetch Pokémon data from the external API and store it in the database.

    This function performs the following tasks:
    1. Sends a request to the Pokémon API to fetch a list of Pokémon.
    2. For each Pokémon in the list, fetches detailed data.
    3. Checks if the Pokémon already exists in the database.
    4. If the Pokémon does not exist, creates a new entry in the database.

    It uses aiohttp for making asynchronous HTTP requests and
    interacts with the database using SQLAlchemy's asynchronous session.
    """
    async with SessionLocal() as db:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://pokeapi.co/api/v2/pokemon?limit=1000") as response:
                data = await response.json()
                for result in data["results"]:
                    async with session.get(result["url"]) as poke_response:
                        poke_data = await poke_response.json()
                        pokemon_name = poke_data["name"]

                        existing_pokemon = await get_pokemon_by_name(db, name=pokemon_name)
                        if existing_pokemon:
                            print(f"Pokémon {pokemon_name} already exists in the database. Skipping insert.")
                            continue

                        pokemon = PokemonCreate(
                            name=poke_data["name"],
                            image_url=poke_data["sprites"]["front_default"],
                            type=poke_data["types"][0]["type"]["name"]
                        )
                        await create_pokemon(db, pokemon)

@app.on_event("startup")
async def on_startup():
    """
    Event handler for application startup.

    This function is called when the FastAPI application starts up.
    It performs the following tasks:
    1. Creates all database tables using the SQLAlchemy metadata.
    2. Fetches Pokémon data from the external API and stores it in the database.

    It uses the `engine` to synchronize the database schema and
    then calls `fetch_and_store_pokemons` to populate the database
    with Pokémon data.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await fetch_and_store_pokemons()
