from langgraph.graph import StateGraph, END
from app.translator import translate_to_english, translate_to_user
from app.rag import retrieve_properties
from app.guardrails_output import validate_output
from app.utils import generate_with_llm

class GraphState(dict):
    pass

# Node: Translate user query to English
def translate_input(state: GraphState):
    query = state["query"]
    translated, user_lang = translate_to_english(query)
    return {"translated_query": translated, "user_lang": user_lang}

# Node: Retrieve relevant property documents using RAG
def rag_search(state: GraphState):
    docs = retrieve_properties(state["translated_query"])
    return {"context": docs}

# Node: Generate LLM output using query and retrieved context
def generate(state: GraphState):
    generated_text = generate_with_llm(state["translated_query"], state["context"])
    # Assume generated_text is a dict with 'id' and 'text' fields or raw text
    return {"raw_output": generated_text}

# Node: Validate the generated output via Guardrails
def guardrails_validation(state: GraphState):
    raw_output = state["raw_output"]
    try:
        # If raw_output is a dict with id & text keys
        doc_id = raw_output.get("id") if isinstance(raw_output, dict) else None
        text = raw_output.get("text") if isinstance(raw_output, dict) else raw_output

        # If doc_id is missing, generate a new UUID
        if not doc_id:
            from app.utils import generate_uuid
            doc_id = generate_uuid()

        validated = validate_output(doc_id, text)
        return {"validated_output": validated}
    except Exception as e:
        # Log or handle validation failure as needed
        from app.utils import log_error
        log_error(f"Guardrails validation failed: {e}")
        return {"validated_output": {"id": doc_id, "text": text}}

# Node: Translate validated output back to user's language
def translate_back(state: GraphState):
    validated_output = state["validated_output"]
    user_lang = state.get("user_lang", "en")
    # validated_output expected as dict with 'text' key
    response_text = validated_output.get("text") if isinstance(validated_output, dict) else str(validated_output)
    translated_response = translate_to_user(response_text, user_lang)
    return {"final_response": translated_response}

# Build and compile LangGraph pipeline
def build_langgraph():
    builder = StateGraph(GraphState)

    builder.add_node("translate_input", translate_input)
    builder.add_node("rag_search", rag_search)
    builder.add_node("generate", generate)
    builder.add_node("guardrails_validation", guardrails_validation)
    builder.add_node("translate_back", translate_back)

    builder.set_entry_point("translate_input")
    builder.add_edge("translate_input", "rag_search")
    builder.add_edge("rag_search", "generate")
    builder.add_edge("generate", "guardrails_validation")
    builder.add_edge("guardrails_validation", "translate_back")
    builder.add_edge("translate_back", END)

    return builder.compile()
