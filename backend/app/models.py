from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class KPI(BaseModel):
    id: str
    label: str
    value: float | str
    unit: Optional[str] = None
    change_pct: float
    trend_label: str
    next_step: str

class KPISummary(BaseModel):
    period_days: int
    kpis: List[KPI]
    generated_at: datetime

class DataHealth(BaseModel):
    last_imported_at: Optional[datetime]
    rows_processed: int
    rows_errored: int
    missing_columns: List[str]
    status: str

class ImportJob(BaseModel):
    id: str
    filename: str
    status: str
    created_at: datetime
    rows_processed: int = 0
    rows_errored: int = 0
    errors: List[str] = []

class InsightOneClickAction(BaseModel):
    type: str
    payload: Dict[str, Any]

class Insight(BaseModel):
    id: str
    headline: str
    why: str
    action: str
    impact: str  # High, Medium, Low
    confidence: float
    one_click_action: Optional[InsightOneClickAction] = None
    created_at: datetime

class ClusterPoint(BaseModel):
    user_id: str
    x: float
    y: float

class Cluster(BaseModel):
    cluster_id: int
    label: str
    description: str
    size: int
    recommended_action: str
    sample_coordinates: List[ClusterPoint]

class SegmentationResponse(BaseModel):
    clusters: List[Cluster]
