import pytest
import pandas as pd
from backend.app.services.kpis import compute_kpis
from backend.app.models import KPI

def test_compute_kpis_revenue(monkeypatch):
    data = {
        'date': pd.to_datetime(['2025-12-25', '2025-12-20', '2025-11-25']),
        'amount': [100, 200, 150],
        'source': ['bank', 'bank', 'bank']
    }
    df = pd.DataFrame(data)
    
    monkeypatch.setattr("backend.app.services.kpis.load_all_data", lambda: df)
    
    # We need to mock datetime.now() in kpis.py to make this deterministic
    # But for simplicity, let's assume the test runs "now" relative to the dates above.
    # Actually, kpis.py uses datetime.now(). If I run this test on Dec 26, 2025, it works.
    # But I can't control the system time.
    # I should mock datetime in the service.
    
    # Let's try to mock datetime in the service
    import datetime
    class MockDateTime(datetime.datetime):
        @classmethod
        def now(cls):
            return datetime.datetime(2025, 12, 26)
            
    monkeypatch.setattr("backend.app.services.kpis.datetime", MockDateTime)
    
    summary = compute_kpis(period_days=30)
    revenue_kpi = next(k for k in summary.kpis if k.id == 'revenue')
    
    # Current period (Dec 26 - 30 days = Nov 26 to Dec 26)
    # Dates in range: 12-25 (100), 12-20 (200). Sum = 300.
    # Previous period (Nov 26 - 30 days = Oct 27 to Nov 26)
    # Dates in range: 11-25 (150). Sum = 150.
    
    # Change: (300 - 150) / 150 = 1.0 (100%)
    
    assert revenue_kpi.value == 300
    assert revenue_kpi.change_pct == 100.0
