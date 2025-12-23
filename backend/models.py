from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class MetricResponse(BaseModel):
    metric: str
    value: float | int | str

class ClusterResponse(BaseModel):
    cluster_id: int
    description: str
    size: int
    features: Dict[str, float]

class InsightResponse(BaseModel):
    category: str
    insight: str

class DatasetSummary(BaseModel):
    filename: str
    rows: int
    columns: List[str]
    missing_values: Dict[str, int]
