from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.app.services import ingest
from backend.app.models import ImportJob
from datetime import datetime

router = APIRouter()

@router.post("/upload", response_model=ImportJob)
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    
    content = await file.read()
    job_id = ingest.process_upload(content, file.filename)
    
    return ImportJob(
        id=job_id,
        filename=file.filename,
        status="processing",
        created_at=datetime.now()
    )
