from pydantic import BaseModel, Field
from datetime import datetime

# Model for creating a note (input from form)
class NoteCreate(BaseModel):
    note: str = Field(..., min_length=1, max_length=500, description="Content of the note.")

# Model for a note as stored in the database and displayed
class NoteInDB(BaseModel):
    id: str = Field(..., alias="_id", description="Unique MongoDB identifier.") # Alias _id to id
    note: str
    created_at: datetime

    class Config:
        populate_by_name = True # Allow mapping id to _id
        from_attributes = True # Allow creating model from DB attributes (Pydantic v2+)
        json_schema_extra = {
            "example": {
                "id": "60d0fe4f52f75d001f3b0e3b",
                "note": "This is a sample note content.",
                "created_at": "2023-10-27T10:30:00Z"
            }
        }
