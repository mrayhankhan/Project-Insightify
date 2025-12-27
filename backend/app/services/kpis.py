import pandas as pd
from datetime import datetime, timedelta
from backend.app.models import KPI, KPISummary
import glob
import os

def load_all_data():
    # Load all parquet files from ingestion
    files = glob.glob("backend/data/*.parquet")
    if not files:
        return pd.DataFrame(columns=["date", "user_id", "amount", "source", "views", "likes", "comments", "clicks", "impressions", "cost"])
    
    dfs = []
    for f in files:
        try:
            dfs.append(pd.read_parquet(f))
        except:
            pass
    
    if not dfs:
        return pd.DataFrame()
        
    df = pd.concat(dfs, ignore_index=True)
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    return df

def compute_kpis(period_days: int = 30) -> KPISummary:
    df = load_all_data()
    
    if df.empty:
        return KPISummary(period_days=period_days, kpis=[], generated_at=datetime.now())

    now = datetime.now()
    start = now - timedelta(days=period_days)
    prev_start = start - timedelta(days=period_days)
    
    # Filter for current period
    dfp = df[(df['date'] >= start) & (df['date'] <= now)]
    # Filter for previous period
    prev = df[(df['date'] >= prev_start) & (df['date'] < start)]
    
    kpis = []
    
    # Revenue
    revenue_curr = dfp[dfp['source']=='bank']['amount'].sum() if 'amount' in dfp.columns else 0
    revenue_prev = prev[prev['source']=='bank']['amount'].sum() if 'amount' in prev.columns else 0
    rev_change = ((revenue_curr - revenue_prev) / revenue_prev * 100) if revenue_prev > 0 else 0
    
    kpis.append(KPI(
        id="revenue",
        label=f"Revenue (Last {period_days} days)",
        value=round(revenue_curr, 2),
        unit="USD",
        change_pct=round(rev_change, 1),
        trend_label=f"vs previous {period_days} days",
        next_step="If revenue fell >5%, review top 3 products."
    ))
    
    # Active Customers
    if 'user_id' in dfp.columns:
        cust_curr = dfp['user_id'].nunique()
        cust_prev = prev['user_id'].nunique()
        cust_change = ((cust_curr - cust_prev) / cust_prev * 100) if cust_prev > 0 else 0
        
        kpis.append(KPI(
            id="active_customers",
            label="Active Customers",
            value=cust_curr,
            unit=None,
            change_pct=round(cust_change, 1),
            trend_label=f"vs previous {period_days} days",
            next_step="Run a referral campaign if growth is flat."
        ))
    
    return KPISummary(
        period_days=period_days,
        kpis=kpis,
        generated_at=datetime.now()
    )
