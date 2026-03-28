from pydantic import BaseModel
from typing import Optional


class FoundItem(BaseModel):
    itemName: str
    description: str
    category: str
    color: str
    locationFound: str
    dateFound: str
    contactNumber: str
    status: str


class FoundItemResponse(FoundItem):
    id: str