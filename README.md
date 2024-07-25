# PokeQuery

## Overview

This project provides a REST API to serve a list of Pokémon with their names, images, and types. The API uses FastAPI framework and fetches data from the [PokeAPI](https://pokeapi.co/).

## Features

- Fetch and store Pokémon data from the PokeAPI and serve subsequent requests from the database.
- API versioning (currently v1).
- Filtering Pokémon by name and type.

## Setup Instructions

### 1. Clone the Repository

```
git clone https://github.com/sushankgghimire/PokeQuery
cd PokeQuery
```
### 2. Create and Activate a Virtual Environment

```
python -m venv venv
source venv/bin/activate
```
### 3. Install Dependencies
```
pip install -r requirements.txt
```
### 4. Configure the Database
Using the `.env_example` file, create a `.env` file in the root directory with the following content:
```
DATABASE_URL=postgresql+asyncpg://username:password@localhost/dbname
```

### 5. Run Database migrations
```
alembic upgrade head
```

### 6. Start the FastAPI server
```
uvicorn app.main:app --reload
```
### 7. Access the API at `http://127.0.0.1:8000/api/v1/pokemons` with your name and type query parameters.

## Endpoints

### Version 1

#### `GET /api/v1/pokemons`

- **Description**: Get a list of all Pokémon stored in the database.
- **Query Parameters**:
  - `skip` (optional): Number of Pokémon to skip (pagination).
  - `limit` (optional): Number of Pokémon to return (pagination).
  - `name` (optional): Filter Pokémon by name.
  - `type` (optional): Filter Pokémon by type.
- **Response**: List of Pokémon with their names, images, and types.



