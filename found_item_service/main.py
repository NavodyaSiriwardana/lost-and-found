from fastapi import FastAPI, HTTPException
from models import FoundItem
from service import (
    fetch_all_found_items,
    fetch_found_item_by_id,
    add_found_item,
    edit_found_item,
    remove_found_item
)

app = FastAPI(title="Found Item Service")


@app.get("/")
def read_root():
    return {"message": "Found Item Service is running"}


@app.get("/api/founditems")
def get_found_items():
    return fetch_all_found_items()


@app.get("/api/founditems/{item_id}")
def get_found_item(item_id: str):
    item = fetch_found_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Found item not found")
    return item


@app.post("/api/founditems")
def create_found_item_endpoint(item: FoundItem):
    return add_found_item(item.dict())


@app.put("/api/founditems/{item_id}")
def update_found_item_endpoint(item_id: str, item: FoundItem):
    updated_item = edit_found_item(item_id, item.dict())
    if not updated_item:
        raise HTTPException(status_code=404, detail="Found item not found")
    return updated_item


@app.delete("/api/founditems/{item_id}")
def delete_found_item_endpoint(item_id: str):
    deleted = remove_found_item(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Found item not found")
    return {"message": f"Found item {item_id} deleted successfully"}