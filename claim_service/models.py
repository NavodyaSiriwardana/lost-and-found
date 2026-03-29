from pydantic import BaseModel, Field
from typing import Optional

class ClaimCreate(BaseModel):
    user_id: str = Field(..., description="Student IT Number")
    user_name: str = Field(..., description="Full Name of the student")
    found_item_id: str = Field(..., description="ID of the found item from database")
    item_name: str = Field(..., description="Name of the item (e.g. Blue Pen)")
    proof_description: str = Field(..., description="Details to prove ownership")
    phone_number: str = Field(..., description="Contact number")

class ClaimUpdate(BaseModel):
    status: str = Field(..., description="'Approved', 'Rejected' or 'Handed Over'")
    admin_comments: Optional[str] = None

class ClaimResponse(ClaimCreate):
    id: str
    status: str = "Pending"