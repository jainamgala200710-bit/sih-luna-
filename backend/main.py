from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from backend.api.endpoints import upload, registration, results, dem

# Initialize FastAPI App
app = FastAPI(
    title="LunaAlign Registration API",
    description="Mathematical backend for sub-pixel cross-modal image registration",
    version="1.0.0"
)

# Custom middleware to log requests
@app.middleware("http")
async def log_requests(request, call_next):
    print(f"HTTP Request: {request.method} {request.url}")
    response = await call_next(request)
    print(f"HTTP Response: {response.status_code}")
    return response

# CORS configuration to allow the Vite React frontend (localhost:5173) to communicate
from backend.custom_cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict to actual frontend domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure temporary execution cache directories exist
os.makedirs("backend/cache/images", exist_ok=True)
os.makedirs("backend/cache/results", exist_ok=True)

# Register Sub-Routers
app.include_router(upload.router, prefix="/api/v1/upload", tags=["Ingestion"])
app.include_router(registration.router, prefix="/api/v1/registration", tags=["Execution"])
app.include_router(results.router, prefix="/api/v1/results", tags=["Telemetry"])
app.include_router(dem.router, prefix="/api/v1/dem", tags=["3D DEM"])

@app.get("/health")
def health_check():
    return {"status": "online", "message": "LunaAlign Backend Operational"}