from fastapi import FastAPI, Request, Response, HTTPException
import httpx
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

# API Gateway එක ආරම්භ කිරීම
app = FastAPI(
    title="Campus Lost & Found - API Gateway",
    description="The Front Desk for all microservices",
    version="1.0.0"
)

# අපේ Microservices 4 දුවන Ports වල ලිපිනයන්
SERVICES = {
    "users": "http://localhost:8001",
    "lostitems": "http://localhost:8002",
    "founditems": "http://localhost:8003",
    "claims": "http://localhost:8004",
}

# එන ඕනෑම Request එකක් අදාළ Service එකට යවන පොදු Function එක
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

# 1. User Service එකට යන පාර (Member 1)
@app.api_route("/api/users/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def route_user_service(path: str, request: Request):
    return await forward_request(SERVICES["users"], f"api/users/{path}", request)


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
@app.api_route("/api/founditems/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def route_found_item_service(path: str, request: Request):
    return await forward_request(SERVICES["founditems"], f"api/founditems/{path}", request)

# 4. Claim Service එකට යන පාර (Member 4)
@app.api_route("/api/claims/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def route_claim_service(path: str, request: Request):
    return await forward_request(SERVICES["claims"], f"api/claims/{path}", request)