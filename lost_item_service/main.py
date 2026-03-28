from fastapi import FastAPI, HTTPException
from models import LostItem
from service import (
    get_all_lost_items,
    get_lost_item_by_id,
    create_lost_item,
    update_lost_item,
    delete_lost_item,
    
)

app = FastAPI(title="Lost Item Service")

@app.get("/")
def root():
    return {"message": "Lost Item Service is running"}

@app.get("/api/lostitems")
def get_items():
    return get_all_lost_items()

@app.get("/api/lostitems/{item_id}")
def get_item(item_id: str):
    item = get_lost_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Lost item not found")
    return item

@app.post("/api/lostitems")
def add_item(item: LostItem):
    return create_lost_item(item.model_dump())

@app.put("/api/lostitems/{item_id}")
def edit_item(item_id: str, item: LostItem):
    updated_item = update_lost_item(item_id, item.model_dump())
    if not updated_item:
        raise HTTPException(status_code=404, detail="Lost item not found or not updated")
    return updated_item

@app.delete("/api/lostitems/{item_id}")
def remove_item(item_id: str):
    deleted = delete_lost_item(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Lost item not found")
    return {"message": "Lost item deleted successfully"}