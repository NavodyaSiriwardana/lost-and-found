from fastapi import FastAPI, Request, Response, HTTPException
import httpx
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# --- User Service Models (Swagger UI පෙන්වීමට අවශ්‍යයි) ---
class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    student_id: Optional[str] = None
    role: str = "Student"
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    student_id: Optional[str] = None
    role: Optional[str] = None

# API Gateway ආරම්භ කිරීම
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

# පොදු Request Forwarding Function එක
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
# 1. User Service Routes (Member 1) - Port 8001
# ==========================================

@app.post("/api/users/register", tags=["User Service"])
async def register_user_gateway(item: UserCreate, request: Request):
    return await forward_request(SERVICES["users"], "api/users/register", request)

@app.get("/api/users", tags=["User Service"])
async def get_all_users_gateway(request: Request):
    return await forward_request(SERVICES["users"], "api/users", request)

@app.get("/api/users/{user_id}", tags=["User Service"])
async def get_user_gateway(user_id: str, request: Request):
    return await forward_request(SERVICES["users"], f"api/users/{user_id}", request)

@app.put("/api/users/{user_id}", tags=["User Service"])
async def update_user_gateway(user_id: str, item: UserUpdate, request: Request):
    return await forward_request(SERVICES["users"], f"api/users/{user_id}", request)

@app.delete("/api/users/{user_id}", tags=["User Service"])
async def delete_user_gateway(user_id: str, request: Request):
    return await forward_request(SERVICES["users"], f"api/users/{user_id}", request)

# සටහන: මෙතනින් පහළට අනෙකුත් සාමාජිකයින්ගේ (Lost, Found, Claim) Routes ඇතුළත් කරන්න.