import os
from dotenv import load_dotenv
from pymongo import MongoClient, errors

# Load environment variables from .env file
load_dotenv()

def get_database():
    """
    Initializes and returns the MongoDB client and database.
    """
    mongo_url = os.getenv("MONGO_DB_URL")
    # mongo_url = "mongodb+srv://iec2021066:fPQoLJ8B9YHDH0DI@mycluster.5vyhkoy.mongodb.net/contest-seeker?retryWrites=true&w=majority"
    if not mongo_url:
        raise ValueError("MONGO_URL is not set in the .env file.")

    try:
        # Initialize MongoDB client
        client = MongoClient(mongo_url)
        
        # Check the connection
        client.admin.command('ping')
        print("Connected to MongoDB successfully")

        # Access and return a specific database
        db = client["iot-project"]
        return db
    except errors.ConnectionFailure as e:
        print(f"Error connecting to MongoDB: {e}")
        raise
    except errors.ConfigurationError as e:
        print(f"Configuration error: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise