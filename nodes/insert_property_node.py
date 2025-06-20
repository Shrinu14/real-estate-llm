# nodes/insert_property_node.py

from mongo_client import insert_property

def insert_property_node(inputs: dict) -> dict:
    validated_data = inputs.get("validated", {})
    doc_id = insert_property(validated_data)
    return {"inserted_id": doc_id, "property_data": validated_data}
