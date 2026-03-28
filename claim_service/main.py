from fastapi import FastAPI, HTTPException
from models import ClaimCreate, ClaimUpdate
from service import (
    fetch_all_claims,
    fetch_claim_by_id,
    add_claim,
    edit_claim,
    remove_claim
)

app = FastAPI(title="Claim Service")

@app.get("/")
def read_root():
    return {"message": "Claim Service is running"}

@app.get("/api/claims")
def get_claims():
    return fetch_all_claims()

@app.get("/api/claims/{claim_id}")
def get_claim(claim_id: str):
    item = fetch_claim_by_id(claim_id)
    if not item:
        raise HTTPException(status_code=404, detail="Claim not found")
    return item

@app.post("/api/claims")
def create_claim_endpoint(claim: ClaimCreate):
    return add_claim(claim.dict())

@app.put("/api/claims/{claim_id}")
def update_claim_endpoint(claim_id: str, claim: ClaimUpdate):
    updated = edit_claim(claim_id, claim.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Claim not found")
    return updated

@app.delete("/api/claims/{claim_id}")
def delete_claim_endpoint(claim_id: str):
    if not remove_claim(claim_id):
        raise HTTPException(status_code=404, detail="Claim not found")
    return {"message": "Claim deleted successfully"}