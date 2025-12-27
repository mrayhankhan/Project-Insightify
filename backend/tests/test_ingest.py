import pytest
from backend.app.services.ingest import process_upload
from backend.app.database import init_db, get_db
import os
import json

def test_ingest_flow():
    init_db()
    csv_content = b"date,user_id,amount,source\n2025-01-01,1,100,bank"
    job_id = process_upload(csv_content, "test.csv")
    
    conn = get_db()
    row = conn.execute("SELECT * FROM imports WHERE id=?", (job_id,)).fetchone()
    if row['status'] != 'completed':
        print(f"Ingestion failed with errors: {row['errors']}")
    assert row['status'] == 'completed'
    assert row['rows_processed'] == 1
    
    # Cleanup
    if os.path.exists(f"backend/data/{job_id}.parquet"):
        os.remove(f"backend/data/{job_id}.parquet")
