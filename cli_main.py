from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.rag import add_document, search  # ✅ Uses Chroma
from app.translator import translate_to_english
from app.guardrails_output import validate_property_output
import os
import logging
import json
# --------------------
# Logger Configuration
# --------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("real_estate_api")

# --------------------
# Initialize FastAPI App
# --------------------
app = FastAPI(
    title="Real Estate Search API",
    description="Multilingual RAG-based Real Estate Search using Chroma + Guardrails",
    version="1.0.0",
    openapi_tags=[
        {"name": "Add", "description": "Add new property documents"},
        {"name": "Search", "description": "Search for real estate listings"},
        {"name": "Health", "description": "Health check endpoint"},
        {"name": "Frontend", "description": "Serve frontend React app"},
    ]
)

# --------------------
# CORS Configuration
# --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔒 Use ["https://yourdomain.com"] in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------
# Request Model
# --------------------
class FolderPathInput(BaseModel):
    folder_path : str
    

# --------------------
# Health Check
# --------------------
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "API is healthy"}

# --------------------
# Add Property Document
# --------------------

@app.post("/bulk-ingest", tags=["Add"])
def bulk_ingest_from_folder(data: FolderPathInput):
    folder = data.folder_path

    if not os.path.exists(folder):
        raise HTTPException(status_code=404, detail=f"Folder not found: {folder}")
    
    inserted_ids = []
    failed_files = []

    for filename in os.listdir(folder):
        if filename.endswith(".json"):
            try:
                filepath = os.path.join(folder, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    property_data = json.load(f)

                # Basic structure handling - adjust keys to match your RERA JSON
                title = property_data.get("title", "Unknown Title")
                location = property_data.get("location", "Unknown Location")
                price = property_data.get("price", 0)
                area = property_data.get("area_sqft", 0)
                bedrooms = property_data.get("bedrooms", 0)
                bathrooms = property_data.get("bathrooms", 0)
                description = property_data.get("description", "")
                language = property_data.get("language", "en")

                # Create full text for embedding
                full_text = (
                    f"Title: {title}\n"
                    f"Location: {location}\n"
                    f"Price: {price}\n"
                    f"Area: {area} sqft\n"
                    f"Bedrooms: {bedrooms}\n"
                    f"Bathrooms: {bathrooms}\n"
                    f"Description: {description}"
                )

                if language.lower() != "en":
                    full_text = translate_to_english(full_text)

                doc_id = add_document(full_text)
                if doc_id:
                    inserted_ids.append({"filename": filename, "doc_id": doc_id})
                else:
                    failed_files.append({"filename": filename, "reason": "Insert returned None"})

            except Exception as e:
                logger.exception(f"Failed to process {filename}")
                failed_files.append({"filename": filename, "reason": str(e)})

    return {
        "inserted": inserted_ids,
        "failed": failed_files,
        "total_processed": len(inserted_ids) + len(failed_files)
    }

# --------------------
# Search Properties
# --------------------
@app.get("/search", tags=["Search"])
def search_properties(
    q: str = Query(..., description="Search query for real estate"),
    language: str = "en"
):
    try:
        logger.info(f"Search query received: {q}")
        query = q

        if language.lower() != "en":
            logger.info(f"Translating search query from {language} to English")
            query = translate_to_english(query)

        results = search(query)
        structured = []

        for doc in results:
            try:
                validated = validate_property_output(doc["text"])
                structured.append(validated)
            except Exception as ve:
                logger.warning(f"Validation failed: {ve}")
                structured.append({"error": "Validation failed", "raw_text": doc["text"]})

        return {"results": structured}

    except Exception as e:
        logger.exception("Search failed")
        raise HTTPException(status_code=500, detail=f"Error during search: {e}")

# --------------------
# Serve React Frontend
# --------------------
app.mount("/static", StaticFiles(directory="frontend_build/static"), name="static")

@app.get("/", tags=["Frontend"])
def serve_react_index():
    index_path = "frontend_build/index.html"
    if os.path.exists(index_path):
        logger.info("Serving frontend index.html")
        return FileResponse(index_path)
    logger.warning("React index.html not found")
    return {"error": "Frontend not found"}

@app.get("/{full_path:path}", tags=["Frontend"])
def catch_all(full_path: str):
    fallback = "frontend_build/index.html"
    if os.path.exists(fallback):
        logger.info(f"Fallback route triggered: /{full_path}")
        return FileResponse(fallback)
    return {"error": "Page not found"}
