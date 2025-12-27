import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_dates(n, days=60):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    dates = []
    for _ in range(n):
        random_days = random.randint(0, days)
        dates.append((start_date + timedelta(days=random_days)).strftime('%Y-%m-%d'))
    return dates

def generate_youtube_data(n=5000):
    categories = ['Tech', 'Vlog', 'Education', 'Gaming', 'Music', 'Comedy', 'News', 'Sports', 'Food', 'Travel']
    
    # Realistic Title Generators
    tech_subjects = ["iPhone 16", "RTX 5090", "Tesla Cybertruck", "Python 4.0", "MacBook Pro", "AI Revolution", "ChatGPT 5", "SpaceX Launch"]
    gaming_subjects = ["Minecraft Hardcore", "GTA VI Leak", "Elden Ring DLC", "Valorant Ranked", "Roblox Obby", "Fortnite Update"]
    vlog_subjects = ["Day in my Life", "My Morning Routine", "Moving to NYC", "Van Life Tour", "Wedding Day", "Surprising my Mom"]
    edu_subjects = ["Calculus 101", "History of Rome", "Learn Japanese", "Quantum Physics", "How to Code", "Financial Freedom"]
    
    templates = [
        "Review: {subject} - Is it worth it?",
        "Top 10 {subject} Secrets",
        "I tried {subject} for 7 Days",
        "The Truth About {subject}",
        "{subject} Full Walkthrough",
        "Why {subject} is Broken",
        "Unboxing {subject}",
        "How to Master {subject}",
        "{subject} vs The Competition",
        "My Honest Thoughts on {subject}"
    ]
    
    titles = []
    video_categories = []
    
    for _ in range(n):
        cat = random.choice(categories)
        video_categories.append(cat)
        
        subject = "Something"
        if cat == 'Tech': subject = random.choice(tech_subjects)
        elif cat == 'Gaming': subject = random.choice(gaming_subjects)
        elif cat == 'Vlog': subject = random.choice(vlog_subjects)
        elif cat == 'Education': subject = random.choice(edu_subjects)
        else: subject = f"{cat} Topic"
        
        title = random.choice(templates).format(subject=subject)
        titles.append(title)

    # Generate views using Log-Normal distribution (Power Law)
    views = np.random.lognormal(mean=10, sigma=2, size=n).astype(int)
    views = np.clip(views, 100, 50000000) 
    
    data = {
        'date': generate_dates(n),
        'source': ['youtube'] * n,
        'video_id': [f'YT_{i:05d}' for i in range(n)],
        'title': titles,
        'category': video_categories,
        'views': views,
        'likes': [],
        'comments': [],
        'watch_time_minutes': []
    }
    
    for v in data['views']:
        likes = int(v * np.random.uniform(0.01, 0.08)) 
        comments = int(likes * np.random.uniform(0.05, 0.2))
        
        watch_time = np.random.lognormal(mean=2, sigma=0.5)
        watch_time = np.clip(watch_time, 0.5, 120)
        
        data['likes'].append(likes)
        data['comments'].append(comments)
        data['watch_time_minutes'].append(round(watch_time, 2))
        
    df = pd.DataFrame(data)
    df.to_csv('data/youtube_data.csv', index=False)
    print(f"Generated data/youtube_data.csv with {n} rows")

def generate_ads_data(n=5000):
    brands = ["Nike", "Apple", "Samsung", "Coca-Cola", "Amazon", "Spotify", "Netflix", "Uber", "Airbnb", "Tesla"]
    types = ["Summer Sale", "Black Friday", "Brand Awareness", "Retargeting", "Holiday Special", "New Launch"]
    
    campaign_names = []
    for _ in range(n):
        brand = random.choice(brands)
        ctype = random.choice(types)
        campaign_names.append(f"{brand} - {ctype} {random.randint(2023, 2025)}")

    data = {
        'date': generate_dates(n),
        'source': ['ads'] * n,
        'campaign_id': [f'AD_{i:05d}' for i in range(n)],
        'campaign_name': campaign_names,
        'impressions': np.random.randint(1000, 500000, n),
        'clicks': [],
        'conversions': [],
        'cost': []
    }
    
    for imp in data['impressions']:
        ctr = np.random.beta(2, 50)
        clicks = int(imp * ctr)
        
        conv_rate = np.random.beta(2, 20)
        conversions = int(clicks * conv_rate)
        
        cpc = np.random.uniform(0.5, 5.0)
        cost = clicks * cpc
        
        data['clicks'].append(clicks)
        data['conversions'].append(conversions)
        data['cost'].append(round(cost, 2))
        
    df = pd.DataFrame(data)
    df.to_csv('data/ads_data.csv', index=False)
    print(f"Generated data/ads_data.csv with {n} rows")

def generate_banking_data(n=5000):
    data = {
        'date': generate_dates(n),
        'source': ['bank'] * n,
        'customer_id': [f'CUST_{i:05d}' for i in range(n)],
        'user_id': [f'U_{i:05d}' for i in range(n)], # Added user_id for KPI calc
        'age': np.random.randint(18, 80, n),
        'amount': [], # Renamed/Added for revenue calc
        'transaction_count': np.random.poisson(lam=20, size=n),
        'products_used': np.random.choice([1, 2, 3, 4], size=n, p=[0.5, 0.3, 0.15, 0.05]),
        'churn_flag': []
    }
    
    # Wealth distribution is also Log-Normal
    balances = np.random.lognormal(mean=8, sigma=1.5, size=n)
    data['amount'] = np.round(balances, 2) # Using balance as 'amount' (revenue proxy)
    
    for i in range(n):
        prob = 0.15
        if data['amount'][i] < 1000: prob += 0.2
        if data['products_used'][i] == 1: prob += 0.1
        if data['transaction_count'][i] < 5: prob += 0.2
        if data['age'][i] > 60: prob -= 0.05
        
        prob = min(max(prob, 0), 1)
        data['churn_flag'].append(1 if random.random() < prob else 0)
        
    df = pd.DataFrame(data)
    df.to_csv('data/banking_data.csv', index=False)
    print(f"Generated data/banking_data.csv with {n} rows")

if __name__ == "__main__":
    generate_youtube_data()
    generate_ads_data()
    generate_banking_data()
