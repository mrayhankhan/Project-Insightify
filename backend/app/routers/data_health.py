from fastapi import APIRouter
from backend.app.models import DataHealth
from backend.app.database import get_db
from datetime import datetime

router = APIRouter()

@router.get("/data_health", response_model=DataHealth)
async def get_data_health():
    conn = get_db()
    c = conn.cursor()
    # Get last import
    row = c.execute("SELECT * FROM imports ORDER BY created_at DESC LIMIT 1").fetchone()
    conn.close()
    
    if row:
        return DataHealth(
            last_imported_at=datetime.fromisoformat(row['created_at']) if isinstance(row['created_at'], str) else row['created_at'],
            rows_processed=row['rows_processed'],
            rows_errored=row['rows_errored'],
            missing_columns=[], 
            status=row['status']
        )
    else:
        return DataHealth(
            last_imported_at=None,
            rows_processed=0,
            rows_errored=0,
            missing_columns=[],
            status="no_data"
        )
