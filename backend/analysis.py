import pandas as pd
import numpy as np
from typing import Dict, Any, List
import io

# In-memory storage for uploaded datasets (for simplicity as per requirements)
DATASETS: Dict[str, pd.DataFrame] = {}

def load_dataset(name: str, file_content: bytes) -> Dict[str, Any]:
    """Loads a CSV dataset into memory and returns a summary."""
    try:
        df = pd.read_csv(io.BytesIO(file_content))
        DATASETS[name] = df
        
        summary = {
            "filename": name,
            "rows": len(df),
            "columns": df.columns.tolist(),
            "missing_values": df.isnull().sum().to_dict()
        }
        return summary
    except Exception as e:
        raise ValueError(f"Error loading dataset: {str(e)}")

def get_dataset_preview(name: str, rows: int = 5) -> List[Dict[str, Any]]:
    """Returns a preview of the dataset."""
    if name not in DATASETS:
        raise ValueError(f"Dataset {name} not found")
    
    df = DATASETS[name]
    # Replace NaN with None for JSON serialization
    return df.head(rows).replace({np.nan: None}).to_dict(orient='records')

def get_summary_statistics(name: str) -> Dict[str, Any]:
    """Returns summary statistics for numerical columns."""
    if name not in DATASETS:
        raise ValueError(f"Dataset {name} not found")
        
    df = DATASETS[name]
    return df.describe().to_dict()

def calculate_kpis(name: str) -> Dict[str, Any]:
    """Calculates KPIs based on the dataset type."""
    if name not in DATASETS:
        raise ValueError(f"Dataset {name} not found")
    
    df = DATASETS[name]
    kpis = {}
    
    if name == "youtube":
        kpis["total_views"] = int(df["views"].sum())
        kpis["avg_engagement_rate"] = float(((df["likes"] + df["comments"]) / df["views"]).mean())
        kpis["top_category"] = df["category"].mode()[0]
        
    elif name == "ads":
        kpis["total_impressions"] = int(df["impressions"].sum())
        kpis["avg_ctr"] = float((df["clicks"] / df["impressions"]).mean())
        kpis["avg_conversion_rate"] = float((df["conversions"] / df["clicks"]).mean())
        kpis["total_cost"] = float(df["cost"].sum())
        
    elif name == "banking":
        kpis["avg_balance"] = float(df["account_balance"].mean())
        kpis["churn_rate"] = float(df["churn_flag"].mean())
        kpis["avg_products"] = float(df["products_used"].mean())
        
    return kpis

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def perform_segmentation(name: str, n_clusters: int = 3) -> Dict[str, Any]:
    """Performs K-Means segmentation on the dataset."""
    if name not in DATASETS:
        raise ValueError(f"Dataset {name} not found")
        
    df = DATASETS[name].copy()
    features = []
    
    if name == "youtube":
        features = ["views", "likes", "watch_time_minutes"]
    elif name == "ads":
        features = ["impressions", "clicks", "cost"]
    elif name == "banking":
        features = ["account_balance", "transaction_count", "products_used"]
    else:
        return {"error": "Segmentation not supported for this dataset"}
        
    # Drop rows with missing values in features
    df_clean = df[features].dropna()
    
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df_clean)
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(scaled_data)
    
    df_clean["cluster"] = clusters
    
    # Analyze clusters
    cluster_summary = []
    for i in range(n_clusters):
        cluster_data = df_clean[df_clean["cluster"] == i]
        summary = {
            "cluster_id": int(i),
            "size": int(len(cluster_data)),
            "features": cluster_data[features].mean().to_dict()
        }
        cluster_summary.append(summary)
        
    return {"clusters": cluster_summary}

def generate_insights(name: str) -> List[Dict[str, str]]:
    """Generates rule-based insights."""
    if name not in DATASETS:
        raise ValueError(f"Dataset {name} not found")
        
    df = DATASETS[name]
    insights = []
    
    if name == "youtube":
        avg_views = df["views"].mean()
        high_views = df[df["views"] > avg_views]
        if high_views["watch_time_minutes"].mean() < 10:
            insights.append({"category": "Content Strategy", "insight": "High engagement videos tend to be under 10 minutes."})
        
        most_popular = df["category"].mode()[0]
        insights.append({"category": "Trend", "insight": f"The most popular category is {most_popular}."})

    elif name == "ads":
        high_cost = df[df["cost"] > df["cost"].quantile(0.75)]
        low_conv = high_cost[high_cost["conversions"] < high_cost["conversions"].quantile(0.25)]
        if not low_conv.empty:
             insights.append({"category": "Optimization", "insight": "Certain ad campaigns have high cost but low conversion."})
             
        avg_ctr = (df["clicks"] / df["impressions"]).mean()
        insights.append({"category": "Performance", "insight": f"Average CTR is {avg_ctr:.2%}. Campaigns below this need optimization."})

    elif name == "banking":
        churners = df[df["churn_flag"] == 1]
        if churners["products_used"].mean() < df["products_used"].mean():
            insights.append({"category": "Retention", "insight": "Customers with fewer products show higher churn."})
            
        if churners["account_balance"].mean() < df["account_balance"].mean():
             insights.append({"category": "Risk", "insight": "Lower account balances are correlated with higher churn risk."})
             
    return insights
