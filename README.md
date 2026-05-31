# NYC TLC Fare Intelligence Dashboard

> Parsa Majidifard · Deakin University

End-to-end NYC Yellow Taxi fare prediction dashboard built on a Databricks medallion pipeline (182M → 151M trips, 2022–2026).

## Features

- **Fare Predictor** — XGBoost-powered fare estimate with full breakdown (surcharges, tolls, congestion pricing)
- **Congestion Insights** — Year-over-year, hourly, borough-level, and pre/post congestion pricing analysis
- **Model Performance** — Compare Linear Regression, Random Forest, Neural Network, XGBoost
- **Driver Earnings** — Zone-by-zone effective $/hr analysis, best hours to drive

## Pipeline Stats

| Layer | Rows | Details |
|-------|------|---------|
| Bronze | 182M | 52 parquet files, raw ingest |
| Silver | 151M | Cleaned, null-filtered |
| Gold | 151M | 45 engineered features |

## Model Results

| Model | R² | RMSE | MAE |
|-------|----|------|-----|
| XGBoost | **0.9659** | $2.93 | $0.82 |
| Neural Network | 0.9555 | $3.35 | $0.83 |
| Random Forest | 0.9581 | $3.25 | $1.15 |
| Linear Regression | 0.9183 | $4.54 | $2.29 |

## Local Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set **Main file path** to `app.py`
5. Click **Deploy**

## Data

The dashboard uses pre-aggregated summary statistics derived from the Gold layer.  
To use real data from Databricks, export a sample:

```python
# In Databricks notebook
sample = spark.table("tlc_gold.yellow_enriched").sample(0.005).toPandas()
sample.to_parquet("data/sample/gold_sample.parquet", index=False)
```

Then upload `gold_sample.parquet` to `data/sample/` in this repo.

## Tech Stack

- **Pipeline**: Databricks Community Edition · Spark 4.1.0 · Python 3.12.3
- **Storage**: Unity Catalog (tlc_bronze / tlc_silver / tlc_gold)
- **ML**: XGBoost, scikit-learn, Neural Network
- **Dashboard**: Streamlit · Plotly · Pandas
