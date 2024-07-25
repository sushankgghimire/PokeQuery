from sqlalchemy import Column, Integer, String, Text
from app.database import Base

# model format to be stored to the database
class Pokemon(Base):
    __tablename__ = 'pokemons'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    image_url = Column(String)
    type = Column(String)
