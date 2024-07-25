import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Retrieve the database URL from the environment variables
DATABASE_URL = os.getenv("DATABASE_URL")