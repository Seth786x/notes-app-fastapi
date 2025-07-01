# # This file is illustrative if you choose to separate routes.
# # The actual logic is currently integrated into index.py above for simplicity.

# from fastapi import APIRouter, HTTPException, Depends
# from pymongo import MongoClient
# from bson import ObjectId
# from typing import List, Dict, Any
# from datetime import datetime

# # Import schemas
# from Schemas.note import NoteInDB, NoteCreate, NoteUpdate

# # Assuming db and notes_collection are available (e.g., passed via dependency injection)
# # In a real setup, you'd configure DB access here or get it from a global dependency
# # For this example, we'll assume `get_database` dependency from index.py

# router = APIRouter(
#     prefix="/api/notes",
#     tags=["notes"],
# )

# # Placeholder for a get_database dependency (similar to one in index.py)
# # This would typically be defined in a common place or passed in.
# # For now, this is just for illustration if you were to move the routes here.
# def get_database_dependency():
#     # Placeholder: In a real app, you'd return the notes_collection here
#     # from a properly initialized database client.
#     # This assumes 'notes_collection' is globally accessible or passed in.
#     return None # Replace with actual collection


# # API: Get all notes
# @router.get("/", response_model=List[NoteInDB])
# async def get_all_api_notes(notes_coll: Any = Depends(get_database_dependency)): # Replace with real dependency
#     # Logic identical to what's in index.py for this route
#     try:
#         notes_data = []
#         for doc in notes_coll.find({}).sort("_id", -1):
#             notes_data.append(NoteInDB(id=str(doc["_id"]), note=doc["note"], created_at=doc.get("created_at")))
#         return notes_data
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to fetch notes: {e}")

# # ... other API routes (create, get single, update, delete) would go here ...
# # Their content would be identical to the @app.get("/api/notes") etc. routes in index.py
# # Just replace @app.get with @router.get and remove the 'notes_coll: Any = Depends(get_database)'
# # if get_database_dependency is properly set up.
