from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Schema for creating a note (input model for POST)
class NoteCreate(BaseModel):
    note: str = Field(..., min_length=1, description="Content of the note.")

    class Config:
        json_schema_extra = {
            "example": {
                "note": "Study FastAPI and MongoDB."
            }
        }

# Schema for updating a note (input model for PUT/PATCH)
class NoteUpdate(BaseModel):
    note: Optional[str] = Field(None, min_length=1, description="New content for the note.")

    class Config:
        json_schema_extra = {
            "example": {
                "note": "Updated: Study FastAPI and MongoDB in depth."
            }
        }

# Schema for a note as it appears when retrieved from the DB (output model)
class NoteInDB(BaseModel):
    id: str = Field(..., alias="_id", description="Unique identifier of the note from MongoDB.")
    note: str
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the note was created.")

    class Config:
        populate_by_name = True # Allow Pydantic to recognize 'id' from '_id'
        from_attributes = True  # For Pydantic v2+, allows creating model from attributes
        json_schema_extra = {
            "example": {
                "id": "60d0fe4f52f75d001f3b0e3b",
                "note": "Remember to buy groceries.",
                "created_at": "2023-10-27T10:00:00Z"
            }
        }
