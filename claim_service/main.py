from fastapi import FastAPI, HTTPException, status
from models import ClaimCreate, ClaimUpdate, ClaimInDB
from data_service import claim_collection
from bson import ObjectId
from bson.errors import InvalidId

app = FastAPI(
    title="Claim Service API",
    description="Handles ownership claims, verifications, and approvals for the Lost & Found system.",
    version="1.0.0"
)

# Health Check Endpoint (සර්වර් එක වැඩද බලන්න)
@app.get("/", tags=["Health"])
async def root():
    return {"message": "Claim Service is up and running!"}

# ==========================================
# 1. CREATE CLAIM (Student)
# ==========================================
@app.post("/api/claims/", status_code=status.HTTP_201_CREATED, tags=["Student Actions"])
async def create_claim(claim: ClaimCreate):
    new_claim = ClaimInDB(**claim.dict())
    claim_dict = new_claim.dict(exclude={"created_at"}) 
    
    result = await claim_collection.insert_one(claim_dict)
    
    if result.inserted_id:
        return {
            "message": "Claim submitted successfully! Status is Pending.", 
            "claim_id": str(result.inserted_id)
        }
    raise HTTPException(status_code=500, detail="Database Error: Failed to save claim")

# ==========================================
# 2. GET ALL CLAIMS (Admin)
# ==========================================
@app.get("/api/claims/", tags=["Admin Actions"])
async def get_all_claims():
    claims = []
    cursor = claim_collection.find({})
    async for document in cursor:
        document["_id"] = str(document["_id"])
        claims.append(document)
    return {"total_claims": len(claims), "claims": claims}

# ==========================================
# 3. GET SINGLE CLAIM (Student/Admin)
# ==========================================
@app.get("/api/claims/{claim_id}", tags=["Shared Actions"])
async def get_single_claim(claim_id: str):
    try:
        obj_id = ObjectId(claim_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid Claim ID format.")

    claim = await claim_collection.find_one({"_id": obj_id})
    if claim:
        claim["_id"] = str(claim["_id"])
        return claim
    
    raise HTTPException(status_code=404, detail="Claim not found.")

# ==========================================
# 4. UPDATE CLAIM STATUS (Admin)
# ==========================================
@app.put("/api/claims/{claim_id}", tags=["Admin Actions"])
async def update_claim_status(claim_id: str, update_data: ClaimUpdate):
    try:
        obj_id = ObjectId(claim_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid Claim ID format.")

    result = await claim_collection.update_one(
        {"_id": obj_id},
        {"$set": {
            "status": update_data.status, 
            "admin_comments": update_data.admin_comments
        }}
    )
    
    if result.modified_count == 1:
        return {"message": f"Claim status successfully updated to '{update_data.status}'."}
    
    # වෙනස් කරන්න දෙයක් තිබුණේ නැත්නම් හෝ ID එක වැරදිනම්
    raise HTTPException(status_code=404, detail="Claim not found or status is already identical.")

# ==========================================
# 5. DELETE CLAIM (Student/Admin)
# ==========================================
@app.delete("/api/claims/{claim_id}", tags=["Shared Actions"])
async def delete_claim(claim_id: str):
    try:
        obj_id = ObjectId(claim_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid Claim ID format.")

    result = await claim_collection.delete_one({"_id": obj_id})
    
    if result.deleted_count == 1:
        return {"message": "Claim successfully deleted."}
    
    raise HTTPException(status_code=404, detail="Claim not found.")