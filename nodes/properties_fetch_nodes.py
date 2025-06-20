# fetch_properties_node.py

from mongo_client import get_properties

def fetch_properties_node(inputs: dict) -> dict:
    """
    LangGraph-compatible node to fetch property listings from MongoDB.
    Accepts filters like city, price range, property_type, language, etc.
    Returns a dictionary containing the matching property documents.
    """

    filters = {}

    # Optional search filters
    if "city" in inputs:
        filters["city"] = {"$regex": inputs["city"], "$options": "i"}
    if "state" in inputs:
        filters["state"] = {"$regex": inputs["state"], "$options": "i"}
    if "min_price" in inputs and "max_price" in inputs:
        filters["price"] = {"$gte": inputs["min_price"], "$lte": inputs["max_price"]}
    elif "min_price" in inputs:
        filters["price"] = {"$gte": inputs["min_price"]}
    elif "max_price" in inputs:
        filters["price"] = {"$lte": inputs["max_price"]}
    if "property_type" in inputs:
        filters["property_type"] = inputs["property_type"]
    if "language" in inputs:
        filters["language"] = inputs["language"]

    results = get_properties(filters)
    return {"results": results}
