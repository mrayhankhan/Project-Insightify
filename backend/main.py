from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
from backend import analysis, models, database
from pydantic import BaseModel
import os

app = FastAPI(title="Insightify API", description="Unified Business Analytics Dashboard API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    email: str
    password: str

@app.get("/")
async def root():
    return {"message": "Welcome to Insightify API"}

@app.post("/auth/login")
async def login(request: LoginRequest):
    # Admin Login Hardcoded Check (as requested)
    if request.email == "admin" and request.password == "admin":
        # In a real app, we would return a proper JWT signed by us or Supabase
        # For this simple implementation, we return a mock session object
        return {
            "access_token": "admin-mock-token",
            "token_type": "bearer",
            "user": {
                "id": "admin",
                "email": "admin@insightify.com",
                "role": "admin"
            }
        }
    
    # For regular users, we expect them to use Supabase Auth on frontend
    # But if we needed backend login:
    if database.supabase:
        try:
            res = database.supabase.auth.sign_in_with_password({
                "email": request.email,
                "password": request.password
            })
            return res
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/upload/{dataset_type}", response_model=models.DatasetSummary)
async def upload_dataset(dataset_type: str, file: UploadFile = File(...)):
    """
    Uploads a dataset (youtube, ads, or banking).
    """
    if dataset_type not in ["youtube", "ads", "banking"]:
        raise HTTPException(status_code=400, detail="Invalid dataset type. Must be 'youtube', 'ads', or 'banking'.")
    
    print(f"Received upload request for {dataset_type}")
    content = await file.read()
    try:
        summary = analysis.load_dataset(dataset_type, content)
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/data/{dataset_type}/preview")
async def get_data_preview(dataset_type: str, rows: int = 5):
    try:
        return analysis.get_dataset_preview(dataset_type, rows)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/data/{dataset_type}/stats")
async def get_data_stats(dataset_type: str):
    try:
        return analysis.get_summary_statistics(dataset_type)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/data/{dataset_type}/kpis")
async def get_kpis(dataset_type: str):
    try:
        return analysis.calculate_kpis(dataset_type)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/data/{dataset_type}/segmentation")
async def get_segmentation(dataset_type: str, n_clusters: int = 3):
    try:
        return analysis.perform_segmentation(dataset_type, n_clusters)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/data/{dataset_type}/insights")
async def get_insights(dataset_type: str):
    try:
        return analysis.generate_insights(dataset_type)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
