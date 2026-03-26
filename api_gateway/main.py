from fastapi import FastAPI, Request, Response, HTTPException
import httpx

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
    # සම්පූර්ණ ලිපිනය හැදීම (උදා: http://localhost:8001/api/users/...)
    url = f"{service_url}/{path}"
    
    # User එවපු Data (JSON Body) එක කියවීම
    body = await request.body()
    
    # httpx හරහා අදාළ Service එකට කෝල් එකක් ගැනීම
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=request.method,
                url=url,
                headers=request.headers.raw, # ආපු Headers ඒ විදියටම යවනවා
                content=body,                # ආපු Data ඒ විදියටම යවනවා
                params=request.query_params  # URL එකේ අගට එන කෑලි (?id=1)
            )
            
            # Service එකෙන් ආපු උත්තරය ආපහු User ට යැවීම
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
        except httpx.RequestError:
            # අදාළ Service එක Off වෙලා නම් මේ Error එක දෙනවා
            raise HTTPException(status_code=503, detail="Service is currently down or unavailable.")


# ==========================================
# Routes (දොරටුවෙන් ඇතුලට හරවා යැවීම)
# ==========================================

# 1. User Service එකට යන පාර (Member 1)
@app.api_route("/api/users/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def route_user_service(path: str, request: Request):
    return await forward_request(SERVICES["users"], f"api/users/{path}", request)

# 2. Lost Item Service එකට යන පාර (Member 2)
@app.api_route("/api/lostitems/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def route_lost_item_service(path: str, request: Request):
    return await forward_request(SERVICES["lostitems"], f"api/lostitems/{path}", request)

# 3. Found Item Service එකට යන පාර (Member 3)
@app.api_route("/api/founditems/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def route_found_item_service(path: str, request: Request):
    return await forward_request(SERVICES["founditems"], f"api/founditems/{path}", request)

# 4. Claim Service එකට යන පාර (ඔයාගේ කොටස - Member 4)
@app.api_route("/api/claims/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def route_claim_service(path: str, request: Request):
    return await forward_request(SERVICES["claims"], f"api/claims/{path}", request)