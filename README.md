# Insightify - Unified Business Analytics Dashboard

Insightify is a unified business analytics dashboard that analyzes YouTube engagement, Ads performance, and Banking customer behavior. It demonstrates core data science skills including data cleaning, exploratory data analysis (EDA), K-Means clustering, and rule-based insight generation.

## Features

- **Unified Dashboard**: View KPIs and visualizations for multiple business domains.
- **Data Ingestion**: Upload CSV datasets for analysis.
- **Segmentation**: K-Means clustering to identify customer/viewer segments.
- **Automated Insights**: Rule-based logic to surface actionable business recommendations.
- **Modern UI**: Built with Next.js and Tailwind CSS.

## Tech Stack

- **Backend**: Python, FastAPI, Pandas, Scikit-learn
- **Frontend**: React, Next.js, Tailwind CSS, Recharts
- **Data**: Sample CSV datasets included

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 18+

### 1. Setup Backend

Navigate to the project root:

```bash
cd backend
pip install -r requirements.txt
cd ..
```

Start the FastAPI server:

```bash
uvicorn backend.main:app --reload
```

The API will be available at `http://localhost:8000`.

### 2. Setup Frontend

Open a new terminal and navigate to the frontend directory:

```bash
cd frontend
npm install
npm run dev
```

The application will be available at `http://localhost:3000`.

### 3. Usage

1.  Open `http://localhost:3000` in your browser.
2.  Go to the **Upload Data** page.
3.  Upload the sample CSV files located in the `data/` directory:
    - `youtube_data.csv` -> YouTube Analytics
    - `ads_data.csv` -> Ads Performance
    - `banking_data.csv` -> Banking Customer Data
4.  Explore the **Dashboard**, **Segmentation**, and **Insights** pages.

## Project Structure

- `backend/`: FastAPI application and analysis logic.
- `frontend/`: Next.js frontend application.
- `data/`: Sample datasets.

## License

MIT
