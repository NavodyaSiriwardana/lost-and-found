import time
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse
import httpx
from typing import Any, Dict
from pydantic import BaseModel
from typing import Optional

# Lost Item model for Swagger body display
class LostItem(BaseModel):
    item_name: str
    description: str
    category: Optional[str] = None
    color: Optional[str] = None
    lost_date: Optional[str] = None
    lost_location: Optional[str] = None
    contact_number: Optional[str] = None
    status: str
    
class FoundItem(BaseModel):
    itemName: str
    description: str
    category: Optional[str] = None
    color: Optional[str] = None
    dateFound: Optional[str] = None
    locationFound: Optional[str] = None
    contactNumber: Optional[str] = None
    status: str

# API Gateway එක ආරම්භ කිරීම
app = FastAPI(
    title="Campus Lost & Found - API Gateway",
    description="The Front Desk for all microservices (Professional Explicit Routing)",
    version="2.0.0"
)

# අපේ Microservices 4 දුවන Ports වල ලිපිනයන්
SERVICES = {
    "users": "http://localhost:8001",
    "lostitems": "http://localhost:8002",
    "founditems": "http://localhost:8003",
    "claims": "http://localhost:8004",
}






# ==========================================
# 4. Claim Service Routes (Member 4 - ඔයාගේ කොටස) - Port 8004
async def forward_request(service_url: str, path: str, request: Request):
    url = f"{service_url}/{path}"
    body = await request.body()

    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=request.method,
                url=url,
                headers=request.headers.raw,
                content=body,
                params=request.query_params
            )

            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Service is currently down or unavailable.")


# ==========================================
# Routes
# ==========================================
@app.get("/api/claims/", tags=["Claim Service"])
async def get_all_claims(request: Request):
    return await forward_request(SERVICES["claims"], "api/claims/", request)

@app.get("/api/claims/{claim_id}", tags=["Claim Service"])
async def get_single_claim(claim_id: str, request: Request):
    return await forward_request(SERVICES["claims"], f"api/claims/{claim_id}", request)

@app.post("/api/claims/", tags=["Claim Service"])
async def create_claim(request: Request):
    return await forward_request(SERVICES["claims"], "api/claims/", request)

@app.put("/api/claims/{claim_id}", tags=["Claim Service"])
async def update_claim_status(claim_id: str, request: Request):
    return await forward_request(SERVICES["claims"], f"api/claims/{claim_id}", request)

@app.delete("/api/claims/{claim_id}", tags=["Claim Service"])
async def delete_claim(claim_id: str, request: Request):
    return await forward_request(SERVICES["claims"], f"api/claims/{claim_id}", request)
# 2. Lost Item Service එකට යන පාර (Member 2)

# GET all lost items
@app.get("/api/lostitems")
async def get_lost_items(request: Request):
    return await forward_request(SERVICES["lostitems"], "api/lostitems", request)

# POST new lost item
@app.post("/api/lostitems")
async def create_lost_item(item: LostItem, request: Request):
    return await forward_request(SERVICES["lostitems"], "api/lostitems", request)

# GET one lost item
@app.get("/api/lostitems/{item_id}")
async def get_lost_item(item_id: str, request: Request):
    return await forward_request(SERVICES["lostitems"], f"api/lostitems/{item_id}", request)

# PUT update one lost item
@app.put("/api/lostitems/{item_id}")
async def update_lost_item(item_id: str, item: LostItem, request: Request):
    return await forward_request(SERVICES["lostitems"], f"api/lostitems/{item_id}", request)

# DELETE one lost item
@app.delete("/api/lostitems/{item_id}")
async def delete_lost_item(item_id: str, request: Request):
    return await forward_request(SERVICES["lostitems"], f"api/lostitems/{item_id}", request)


# 3. Found Item Service එකට යන පාර (Member 3)
# GET all found items
# GET all found items
@app.get("/api/founditems")
async def get_found_items(request: Request):
    return await forward_request(SERVICES["founditems"], "api/founditems", request)

# POST new found item
@app.post("/api/founditems")
async def create_found_item(item: FoundItem, request: Request):
    return await forward_request(SERVICES["founditems"], "api/founditems", request)

# GET one found item
@app.get("/api/founditems/{item_id}")
async def get_found_item(item_id: str, request: Request):
    return await forward_request(SERVICES["founditems"], f"api/founditems/{item_id}", request)

# PUT update one found item
@app.put("/api/founditems/{item_id}")
async def update_found_item(item_id: str, item: FoundItem, request: Request):
    return await forward_request(SERVICES["founditems"], f"api/founditems/{item_id}", request)

# DELETE one found item
@app.delete("/api/founditems/{item_id}")
async def delete_found_item(item_id: str, request: Request):
    return await forward_request(SERVICES["founditems"], f"api/founditems/{item_id}", request)


