import pandas as pd
import numpy as np
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_youtube_data(n=200):
    categories = ['Tech', 'Vlog', 'Education', 'Gaming', 'Music']
    data = {
        'video_id': [f'YT_{i:03d}' for i in range(n)],
        'title': [f'Video Title {i}' for i in range(n)],
        'category': [random.choice(categories) for _ in range(n)],
        'views': np.random.randint(100, 1000000, n),
        'likes': [],
        'comments': [],
        'watch_time_minutes': np.random.uniform(1, 60, n).round(2)
    }
    
    # Correlate likes and comments with views
    for v in data['views']:
        data['likes'].append(int(v * np.random.uniform(0.01, 0.1)))
        data['comments'].append(int(v * np.random.uniform(0.001, 0.01)))
        
    df = pd.DataFrame(data)
    df.to_csv('data/youtube_data.csv', index=False)
    print("Generated data/youtube_data.csv")

def generate_ads_data(n=200):
    campaigns = ['Summer Sale', 'Black Friday', 'New Launch', 'Brand Awareness', 'Retargeting']
    data = {
        'campaign_id': [f'AD_{i:03d}' for i in range(n)],
        'campaign_name': [random.choice(campaigns) for _ in range(n)],
        'impressions': np.random.randint(1000, 100000, n),
        'clicks': [],
        'conversions': [],
        'cost': []
    }
    
    for imp in data['impressions']:
        clicks = int(imp * np.random.uniform(0.01, 0.05)) # CTR 1-5%
        conversions = int(clicks * np.random.uniform(0.05, 0.2)) # Conv Rate 5-20%
        cost = clicks * np.random.uniform(0.5, 5.0) # CPC $0.5 - $5.0
        
        data['clicks'].append(clicks)
        data['conversions'].append(conversions)
        data['cost'].append(round(cost, 2))
        
    df = pd.DataFrame(data)
    df.to_csv('data/ads_data.csv', index=False)
    print("Generated data/ads_data.csv")

def generate_banking_data(n=200):
    data = {
        'customer_id': [f'CUST_{i:03d}' for i in range(n)],
        'age': np.random.randint(18, 70, n),
        'account_balance': np.random.uniform(100, 50000, n).round(2),
        'transaction_count': np.random.randint(0, 100, n),
        'products_used': np.random.randint(1, 5, n),
        'churn_flag': []
    }
    
    # Churn logic: lower balance/products -> higher churn probability
    for i in range(n):
        prob = 0.1
        if data['account_balance'][i] < 1000: prob += 0.3
        if data['products_used'][i] == 1: prob += 0.2
        if data['transaction_count'][i] < 5: prob += 0.2
        
        data['churn_flag'].append(1 if random.random() < prob else 0)
        
    df = pd.DataFrame(data)
    df.to_csv('data/banking_data.csv', index=False)
    print("Generated data/banking_data.csv")

if __name__ == "__main__":
    generate_youtube_data()
    generate_ads_data()
    generate_banking_data()
