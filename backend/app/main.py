from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routers import upload, kpis, data_health
from backend.app.database import init_db
import os

app = FastAPI(title="Insightify API", description="Friendly Analytics API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()
    os.makedirs("backend/data", exist_ok=True)

app.include_router(upload.router, prefix="/api", tags=["Upload"])
app.include_router(kpis.router, prefix="/api", tags=["KPIs"])
app.include_router(data_health.router, prefix="/api", tags=["Data Health"])

@app.get("/")
def root():
    return {"message": "Insightify Friendly API is running"}
