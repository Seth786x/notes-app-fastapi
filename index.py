import os # Make sure this line is at the top
from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from bson import ObjectId
from datetime import datetime
from typing import Any, Optional
from pathlib import Path

# Import your Pydantic models
from Models.note import NoteCreate, NoteInDB

# --- FastAPI App Initialization ---
app = FastAPI(
    title="Simple FastAPI Notes App",
    description="A basic CRUD application for notes with MongoDB."
)

# --- Configuration ---
# THIS IS THE KEY CHANGE: Use an environment variable for MONGO_DETAILS
MONGO_DETAILS = os.getenv("MONGO_DETAILS", "mongodb+srv://Seth786x:Blueskyl%40ke7@cc.isfpd1c.mongodb.net/")
DATABASE_NAME = "simple_notes_db"
COLLECTION_NAME = "notes"

# --- MongoDB Connection ---
client: Optional[MongoClient] = None
notes_collection: Any = None
try:
    client = MongoClient(MONGO_DETAILS, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    db = client[DATABASE_NAME]
    notes_collection = db[COLLECTION_NAME]
    print("MongoDB connection successful!")
except ServerSelectionTimeoutError as e:
    print(f"MongoDB server selection timed out: {e}")
    client = None
    notes_collection = None
except ConnectionFailure as e:
    print(f"MongoDB connection failed: {e}")
    client = None
    notes_collection = None


# --- Templates and Static Files Setup ---
BASE_DIR = Path(__file__).resolve().parent

# --- DEBUG PRINTS START (You can remove these after verifying paths) ---
print(f"\n--- Debugging Paths ---")
print(f"BASE_DIR (where index.py is): {BASE_DIR}")
print(f"Expected templates directory: {BASE_DIR / 'templates'}")
print(f"Expected static directory (used in code): {BASE_DIR / 'static'}")
print(f"Does templates directory exist? {(BASE_DIR / 'templates').exists()}")
print(f"Does static directory exist? {(BASE_DIR / 'static').exists()}")
print(f"--- Debugging Paths End ---\n")
# --- DEBUG PRINTS END ---

templates = Jinja2Templates(directory=BASE_DIR / "templates")
static_directory = BASE_DIR / "static"
app.mount("/static", StaticFiles(directory=static_directory), name="static")


# --- Dependency to get DB collection ---
def get_database_collection():
    if notes_collection is None:
        raise HTTPException(status_code=500, detail="Database connection not established. Check MongoDB logs.")
    return notes_collection

# --- Web UI Routes ---

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, notes_coll: Any = Depends(get_database_collection)):
    """Displays the main page with all notes."""
    try:
        notes_from_db = []
        for doc in notes_coll.find({}).sort("_id", -1):
            doc["_id"] = str(doc["_id"])
            if "created_at" not in doc:
                doc["created_at"] = datetime.utcnow()
            notes_from_db.append(NoteInDB.model_validate(doc))
        return templates.TemplateResponse("index.html", {"request": request, "notes": notes_from_db})
    except Exception as e:
        print(f"Error fetching notes for root: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve notes.")

@app.post("/add-note", response_class=RedirectResponse, status_code=303)
async def add_note_form(note_content: str = Form(..., alias="note"), notes_coll: Any = Depends(get_database_collection)):
    """Handles adding a new note from the HTML form."""
    try:
        new_note_data = NoteCreate(note=note_content)
        note_dict = new_note_data.model_dump()
        note_dict["created_at"] = datetime.utcnow()

        notes_coll.insert_one(note_dict)
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        print(f"Error adding note from form: {e}")
        raise HTTPException(status_code=500, detail="Failed to add note.")

@app.post("/delete-note/{note_id}", response_class=RedirectResponse, status_code=303)
async def delete_note_form(note_id: str, notes_coll: Any = Depends(get_database_collection)):
    """Handles deleting a note from the HTML form."""
    try:
        if not ObjectId.is_valid(note_id):
            raise HTTPException(status_code=400, detail="Invalid Note ID format.")

        result = notes_coll.delete_one({"_id": ObjectId(note_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Note not found.")

        return RedirectResponse(url="/", status_code=303)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error deleting note from form: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete note.")