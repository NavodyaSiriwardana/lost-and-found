import time
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import httpx
from typing import Any, Dict

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

# එන ඕනෑම Request එකක් අදාළ Service එකට යවන පොදු Function එක
async def forward_request(service: str, path: str, method: str, body: dict = None) -> Any:
    if service not in SERVICES:
        raise HTTPException(status_code=404, detail=f"Service '{service}' is not registered.")

    url = f"{SERVICES[service]}{path}"

    async with httpx.AsyncClient() as client:
        try:
            if method == "GET":
                response = await client.get(url)
            elif method == "POST":
                response = await client.post(url, json=body)
            elif method == "PUT":
                response = await client.put(url, json=body)
            elif method == "DELETE":
                response = await client.delete(url)
            else:
                raise HTTPException(status_code=405, detail="HTTP Method not allowed")

            if response.status_code >= 400:
                return JSONResponse(
                    content=response.json() if response.text else {"detail": "Error from service"},
                    status_code=response.status_code
                )

            return JSONResponse(
                content=response.json() if response.text else None,
                status_code=response.status_code
            )
            
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail=f"The {service} service is offline. Please start it on its port.")




# ==========================================
# 4. Claim Service Routes (Member 4 - ඔයාගේ කොටස) - Port 8004
# ==========================================
@app.get("/api/claims/", tags=["Claim Service"])
async def get_all_claims(): return await forward_request("claims", "/api/claims/", "GET")

@app.get("/api/claims/{claim_id}", tags=["Claim Service"])
async def get_single_claim(claim_id: str): return await forward_request("claims", f"/api/claims/{claim_id}", "GET")

@app.post("/api/claims/", tags=["Claim Service"])
async def create_claim(body: Dict[str, Any]): return await forward_request("claims", "/api/claims/", "POST", body)

@app.put("/api/claims/{claim_id}", tags=["Claim Service"])
async def update_claim_status(claim_id: str, body: Dict[str, Any]): return await forward_request("claims", f"/api/claims/{claim_id}", "PUT", body)

@app.delete("/api/claims/{claim_id}", tags=["Claim Service"])
async def delete_claim(claim_id: str): return await forward_request("claims", f"/api/claims/{claim_id}", "DELETE")