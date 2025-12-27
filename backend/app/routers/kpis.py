from fastapi import APIRouter, Query
from backend.app.services import kpis
from backend.app.models import KPISummary

router = APIRouter()

@router.get("/kpis", response_model=KPISummary)
async def get_kpis(period: int = Query(30, description="Period in days")):
    return kpis.compute_kpis(period_days=period)
