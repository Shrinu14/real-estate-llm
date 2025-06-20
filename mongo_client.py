# mongo_client.py

import os
from pymongo import MongoClient

# Load Mongo URI from environment or use default
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://mongo:27017/")


# Initialize MongoDB client
client = MongoClient(MONGO_URI)
db = client["real_estate"]
properties_collection = db["properties"]
# client = MongoClient(MONGO_URI)

def insert_property(property_data: dict) -> str:
    """
    Inserts a validated property document into the MongoDB collection.
    Returns the inserted document's ID as a string.
    """
    result = properties_collection.insert_one(property_data)
    return str(result.inserted_id)

def get_properties(filters: dict = {}, projection: dict = None) -> list:
    """
    Retrieves property documents from MongoDB matching the filters.
    """
    if projection is None:
        projection = {"_id": 0}  # Hide MongoDB's internal _id field by default

    return list(properties_collection.find(filters, projection))
