from fastapi import FastAPI
from app.routers import pokemon_v1
import aiohttp
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import engine, Base, SessionLocal
from app.models import Pokemon
from app.schemas import PokemonCreate
from app.crud import create_pokemon, get_pokemons, get_pokemon_by_name

app = FastAPI()

app.include_router(pokemon_v1.router, prefix="/api/v1")

async def fetch_and_store_pokemons():
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
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await fetch_and_store_pokemons()
