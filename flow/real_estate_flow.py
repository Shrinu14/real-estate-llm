# flow/real_estate_flow.py

from langgraph.graph import StateGraph
from nodes.guardrails_validate import validate_with_guardrails
from nodes.insert_property_node import insert_property_node
from nodes.fetch_properties_node import fetch_properties_node

# Step 1: Define flow
builder = StateGraph()

builder.add_node("guardrails_validate", validate_with_guardrails)
builder.add_node("insert_to_mongo", insert_property_node)
builder.add_node("fetch_from_mongo", fetch_properties_node)

# Step 2: Set transitions
builder.set_entry_point("guardrails_validate")
builder.add_edge("guardrails_validate", "insert_to_mongo")
builder.add_edge("insert_to_mongo", "fetch_from_mongo")

# Step 3: Compile the DAG
graph = builder.compile()
