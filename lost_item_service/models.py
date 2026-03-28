from pydantic import BaseModel
from typing import Optional

class LostItem(BaseModel):
    item_name: str
    description: Optional[str] = None
    category: Optional[str] = None
    color: Optional[str] = None
    lost_date: Optional[str] = None
    lost_location: Optional[str] = None
    contact_number: Optional[str] = None
    status: Optional[str] = "Pending"
    