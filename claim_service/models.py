from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# 1. Student Request DTO (අලුත් Claim එකක් දාද්දී)
class ClaimCreate(BaseModel):
    user_id: str = Field(..., description="ID of the user making the claim")
    found_item_id: str = Field(..., description="ID of the found item")
    lost_item_id: Optional[str] = Field(None, description="ID of the lost item report (Optional)")
    item_name: str = Field(..., description="Short name of the item")
    proof_description: str = Field(..., description="Evidence to prove ownership")
    phone_number: str = Field(..., description="Contact number")

    # Swagger UI එකේ පේන ලස්සන Example එක
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "101",
                "found_item_id": "F-500",
                "lost_item_id": "L-100",
                "item_name": "MSI Black Bag",
                "proof_description": "It has a batman sticker on the back pocket.",
                "phone_number": "0771234567"
            }
        }

# 2. Admin Update DTO (Status එක වෙනස් කරද්දී)
class ClaimUpdate(BaseModel):
    status: str = Field(..., description="'Approved', 'Rejected', or 'Handed Over'")
    admin_comments: Optional[str] = Field(None, description="Reason for the decision")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "Approved",
                "admin_comments": "Proof verified. Sticker is present."
            }
        }

# 3. Database Entity (MongoDB එකේ සේව් වෙන හැඩය)
class ClaimInDB(BaseModel):
    user_id: str
    found_item_id: str
    lost_item_id: Optional[str] = None
    item_name: str
    proof_description: str
    phone_number: str
    status: str = "Pending"
    admin_comments: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)