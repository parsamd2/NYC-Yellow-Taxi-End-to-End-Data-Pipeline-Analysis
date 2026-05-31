# NYC TLC Fare Intelligence

> Parsa Majidifard · Deakin University

![Python](https://img.shields.io/badge/Python-3.12.3-3776AB?style=flat-square&logo=python&logoColor=white)
![Spark](https://img.shields.io/badge/Apache_Spark-4.1.0-E25A1C?style=flat-square&logo=apachespark&logoColor=white)
![Databricks](https://img.shields.io/badge/Databricks-Community_Edition-FF3621?style=flat-square&logo=databricks&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![XGBoost R²](https://img.shields.io/badge/XGBoost_R²-0.9659-22C55E?style=flat-square)
![Trips](https://img.shields.io/badge/Trips_Processed-151M-6366F1?style=flat-square)

End-to-end data engineering and machine learning pipeline on **151 million NYC Yellow Taxi trips (2022–2026)**. Built a Medallion architecture on Databricks — Bronze → Silver → Gold — then trained four fare prediction models and deployed an interactive Streamlit dashboard.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Data Source](#2-data-source)
3. [Medallion Architecture](#3-medallion-architecture)
4. [Feature Engineering — Gold Layer](#4-feature-engineering--gold-layer)
5. [Model Results](#5-model-results)
6. [Key Findings](#6-key-findings)
7. [Dashboard](#7-dashboard)
8. [Tech Stack](#8-tech-stack)
9. [Running Locally](#9-running-locally)

---

## 1. Project Overview

This project answers three questions using the full NYC TLC trip record dataset:

- **What factors drive taxi fare prices?** — Trained four regression models; XGBoost achieves R² = 0.9659 (RMSE $2.93) using 45 engineered features.
- **How has urban congestion changed?** — Congestion share rose from 35.57% (2022) to 42.29% (2026), costing 14.48 million hours of travel time.
- **Where do drivers earn the most?** — Airport-adjacent zones dominate; EWR achieves an effective rate of $648/hr due to high flat fares and short queue times.

The pipeline ingests raw Parquet files from the TLC open data portal, applies a two-stage cleaning and enrichment process in Spark, trains models in Databricks, and exposes results through a dark-themed Streamlit dashboard.

---

## 2. Data Source

| Attribute | Detail |
|-----------|--------|
| Source | [NYC Taxi & Limousine Commission — Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) |
| Vehicle type | Yellow Medallion Taxi |
| Date range | January 2022 – March 2026 |
| Raw files | 52 monthly Parquet files |
| Raw row count | ~182 million trips |
| Final row count (post-cleaning) | ~151 million trips |
| Storage | DBFS / Unity Catalog on Databricks Community Edition |

---

## 3. Medallion Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│  RAW PARQUET  (52 files, TLC open data portal)                       │
└───────────────────────────┬──────────────────────────────────────────┘
                            │ Spark ingest
                            ▼
┌──────────────────────────────────────────────────────────────────────┐
│  BRONZE  ·  tlc_bronze.yellow_raw                                    │
│  182M rows  ·  Schema-on-read  ·  No transformations                 │
│  Preserves full fidelity of source data                              │
└───────────────────────────┬──────────────────────────────────────────┘
                            │ Cleaning & validation
                            ▼
┌──────────────────────────────────────────────────────────────────────┐
│  SILVER  ·  tlc_silver.yellow_clean                                  │
│  151M rows  ·  31M rows removed (~17%)                               │
│  · Null / missing field removal                                      │
│  · Fare amount bounds enforced ($3 – $500)                           │
│  · Trip distance bounds (0.1 – 100 miles)                            │
│  · Duration bounds (1 – 300 minutes)                                 │
│  · Passenger count bounds (1 – 6)                                    │
│  · Future-dated and pre-2022 records dropped                         │
└───────────────────────────┬──────────────────────────────────────────┘
                            │ Feature engineering
                            ▼
┌──────────────────────────────────────────────────────────────────────┐
│  GOLD  ·  tlc_gold.yellow_enriched                                   │
│  151M rows  ·  45 engineered features  ·  Model-ready                │
│  · Temporal decomposition and cyclic encoding                        │
│  · Borough and zone mapping (TLC zone lookup)                        │
│  · Congestion share computation                                      │
│  · Route-level aggregated fare statistics                            │
│  · Surcharge and pricing flag engineering                            │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 4. Feature Engineering — Gold Layer

All 45 features present in `tlc_gold.yellow_enriched`:

### Trip Metrics (7)

| Feature | Description |
|---------|-------------|
| `trip_distance` | Haversine-corrected trip distance in miles |
| `trip_duration_mins` | Total elapsed time from pickup to dropoff |
| `avg_speed_mph` | `trip_distance / (trip_duration_mins / 60)` |
| `distance_ratio` | Trip distance relative to straight-line borough mean |
| `passenger_count` | Number of passengers (1–6) |
| `tip_pct` | `tip_amount / fare_amount` — tip rate proxy |
| `effective_speed_ratio` | `avg_speed_mph / borough_avg_speed_mph` |

### Temporal (11)

| Feature | Description |
|---------|-------------|
| `pickup_year` | Calendar year (2022–2026) |
| `pickup_month` | Month of year (1–12) |
| `pickup_hour` | Hour of day (0–23) |
| `pickup_dow` | Day of week (0 = Monday, 6 = Sunday) |
| `is_rush_hour` | 1 if weekday AM rush (07–09) or PM rush (16–19) |
| `is_weekend` | 1 if Saturday or Sunday |
| `is_night` | 1 if pickup hour between 22:00 and 05:00 |
| `hour_sin` | `sin(2π · pickup_hour / 24)` — cyclic encoding |
| `hour_cos` | `cos(2π · pickup_hour / 24)` — cyclic encoding |
| `dow_sin` | `sin(2π · pickup_dow / 7)` — cyclic encoding |
| `dow_cos` | `cos(2π · pickup_dow / 7)` — cyclic encoding |

### Location & Route (8)

| Feature | Description |
|---------|-------------|
| `PULocationID` | TLC pickup zone ID (1–265) |
| `DOLocationID` | TLC dropoff zone ID (1–265) |
| `PUBorough` | Pickup borough (Manhattan / Brooklyn / Queens / Bronx / Staten Island / EWR) |
| `DOBorough` | Dropoff borough |
| `is_cbd_pickup` | 1 if pickup zone is in the Manhattan central business district |
| `is_cbd_dropoff` | 1 if dropoff zone is in the Manhattan CBD |
| `route_mean_fare` | Mean historical fare for the PU→DO zone pair |
| `route_trip_count` | Number of historical trips on the PU→DO zone pair |

### Congestion (3)

| Feature | Description |
|---------|-------------|
| `congestion_share` | Fraction of trip time spent in congested conditions |
| `is_post_congestion` | 1 if pickup date ≥ January 2025 (congestion pricing era) |
| `is_rush_congestion` | 1 if `is_rush_hour AND congestion_share > 0.5` |

### Financial (10)

| Feature | Description |
|---------|-------------|
| `fare_amount` | Metered base fare per TLC rate schedule |
| `tip_amount` | Tip amount (credit card trips only) |
| `total_amount` | Total charged including all surcharges and tolls |
| `extra` | Miscellaneous extras (overnight, rush-hour surcharges) |
| `mta_tax` | $0.50 MTA state surcharge |
| `tolls_amount` | Bridge and tunnel tolls |
| `improvement_surcharge` | $0.30 trip improvement surcharge |
| `congestion_surcharge` | $2.75 NYC congestion surcharge (pre-2025 pricing zone) |
| `airport_fee` | Flat airport access fee (JFK/LaGuardia) |
| `is_airport_trip` | 1 if either endpoint is an airport zone |

### Categorical (6)

| Feature | Description |
|---------|-------------|
| `VendorID` | Technology provider (1 = Creative Mobile, 2 = VeriFone) |
| `RatecodeID` | Rate code (1=Standard, 2=JFK, 3=Newark, 4=Nassau, 5=Negotiated, 6=Group) |
| `payment_type` | 1=Credit card, 2=Cash, 3=No charge, 4=Dispute |
| `is_credit_card` | 1 if `payment_type == 1` (tip data available) |
| `store_and_fwd_flag` | Y/N — whether trip record was held in vehicle memory before send |
| `is_shared_ride` | 1 if `RatecodeID == 6` (group ride) |

---

## 5. Model Results

All models trained on the Gold layer (151M trips). 80/20 train/test split, stratified by year.

| Model | R² | RMSE | MAE | MAPE | Notes |
|-------|----|------|-----|------|-------|
| **XGBoost** | **0.9659** | **$2.93** | **$0.82** | **5.39%** | Best across all metrics |
| Random Forest | 0.9581 | $3.25 | $1.15 | — | Strong but slower to train |
| Neural Network | 0.9555 | $3.35 | $0.83 | 4.57% | Comparable MAE; higher RMSE |
| Linear Regression | 0.9183 | $4.54 | $2.29 | — | Baseline; underperforms on airport trips |

**Why XGBoost wins:** Gradient boosting captures non-linear interactions between `route_mean_fare`, `is_post_congestion`, and the cyclic time features that linear regression cannot model and that the neural network requires more data to learn. Its residual distribution is tightly centred at zero with the lowest spread of all four models.

**Top XGBoost feature importances (by gain):**
1. `route_mean_fare` — encodes historical zone-pair pricing signal
2. `trip_distance` — primary metering input
3. `trip_duration_mins` — time component of metered fare
4. `is_airport_trip` — large discrete fare jump
5. `hour_cos` / `hour_sin` — captures intraday demand patterns

---

## 6. Key Findings

### Congestion Trends

| Year | Congestion Share | Avg Fare | Hours Lost (M) |
|------|-----------------|----------|----------------|
| 2022 | 35.57% | $13.21 | 2.41M |
| 2023 | 37.12% | $14.05 | 2.73M |
| 2024 | 38.84% | $14.88 | 2.98M |
| 2025 | 40.91% | $16.43 | 3.21M |
| 2026 | 42.29% | $17.02 | 3.15M |

Across all 151M trips, **14.48 million hours** were lost to congestion — the equivalent of over 1,600 years of cumulative travel time.

### Borough Congestion

| Borough | Avg Congestion | Avg Speed | Trips (M) |
|---------|---------------|-----------|-----------|
| Manhattan | 51.2% | 9.38 mph | 78.2M |
| Brooklyn | 38.4% | 13.2 mph | 28.4M |
| Queens | 34.7% | 15.6 mph | 24.6M |
| Bronx | 29.1% | 16.8 mph | 12.1M |
| Staten Island | 22.3% | 21.4 mph | 3.8M |

### Congestion Pricing Impact (January 2025)

NYC's congestion pricing scheme took effect on 5 January 2025, charging a $9 entry fee for vehicles entering the Manhattan CBD south of 60th Street.

| Metric | Pre-Jan 2025 | Post-Jan 2025 | Change |
|--------|-------------|---------------|--------|
| Avg fare | $14.31 | $15.99 | **+$1.68** |
| Avg tip | $2.87 | $3.12 | +$0.25 |
| CBD avg speed | 10.13 mph | 9.38 mph | −0.75 mph |
| Congestion share | 38.84% | 41.60% | +2.76pp |

> **Selection effect:** The $9 entry fee priced out short, low-value CBD trips, leaving only longer, higher-fare journeys in the dataset. This explains the apparent paradox of higher average fares alongside *lower* average speeds — the trip composition changed, not the road conditions.

### Airport Premium

| Trip Type | Avg Fare | Avg Tip % | Avg Duration |
|-----------|----------|-----------|--------------|
| Airport | $52.52 | 18.2% | 38.4 min |
| CBD Only | $19.80 | 16.8% | 22.1 min |
| Rush Hour | $17.40 | 15.9% | 28.6 min |
| Night (2–4 AM) | $15.20 | 14.2% | 18.2 min |
| Non-Airport | $14.11 | 14.6% | 19.8 min |

Airport trips command a **3.7× fare premium** over non-airport trips.

### Driver Earnings by Zone

| Zone | Effective $/hr | Avg Fare | Avg Duration |
|------|---------------|----------|--------------|
| EWR (Newark) | **$648/hr** | $52.52 | 28.4 min |
| JFK Airport | $412/hr | $48.30 | 42.1 min |
| LaGuardia | $387/hr | $31.20 | 21.6 min |
| Midtown Manhattan | $298/hr | $18.40 | 18.2 min |
| Times Square | $276/hr | $16.80 | 14.1 min |
| Upper East Side | $241/hr | $22.10 | 19.8 min |
| Downtown Brooklyn | $198/hr | $14.20 | 14.4 min |
| Astoria, Queens | $176/hr | $13.80 | 14.2 min |

EWR leads despite lower fares than JFK because the Newark taxi stand has significantly shorter queue times — drivers spend less time waiting and more time earning.

---

## 7. Dashboard

A five-page Streamlit app exposing all pipeline outputs interactively.

| Page | Description |
|------|-------------|
| **Overview** | Pipeline stats, medallion layer summary, model comparison, top findings |
| **Fare Predictor** | Rule-based XGBoost approximation: select borough, distance, time, airport flag — get a fare estimate with full surcharge breakdown |
| **Congestion Insights** | Year-over-year trends, hourly heatmap, borough breakdown, pre/post congestion pricing comparison |
| **Model Performance** | Metrics table, predicted vs actual scatter, residual distribution for all four models |
| **Driver Earnings** | Zone-level effective $/hr ranking, trip type breakdown, best hours to drive |

---

## 8. Tech Stack

| Layer | Tools |
|-------|-------|
| Compute | Databricks Community Edition |
| Processing | Apache Spark 4.1.0 |
| Language | Python 3.12.3 |
| Storage | Unity Catalog — `tlc_bronze` / `tlc_silver` / `tlc_gold` |
| ML | XGBoost 2.x · scikit-learn 1.3 · PyTorch (Neural Network) |
| Dashboard | Streamlit ≥ 1.32 · Plotly ≥ 5.18 · Pandas ≥ 2.0 |
| Data I/O | PyArrow (Parquet) |

---

## 9. Running Locally

The dashboard uses pre-aggregated inline data and does not require a Databricks connection to run.

```bash
# Clone and install
git clone https://github.com/parsamd2/NYC-Yellow-Taxi-End-to-End-Data-Pipeline-Analysis.git
cd NYC-Yellow-Taxi-End-to-End-Data-Pipeline-Analysis
pip install -r requirements.txt

# Launch
streamlit run app.py
```

The app opens at `http://localhost:8501`.

### Using Real Gold Layer Data (optional)

To connect live Databricks exports, run `data/export_from_databricks.py` inside a Databricks notebook after the pipeline completes. This generates five files:

| File | Contents |
|------|----------|
| `gold_sample.parquet` | ~750K row sample (0.5% of Gold) for the fare predictor |
| `congestion_by_year.csv` | Annual congestion aggregates |
| `congestion_by_hour.csv` | Hourly congestion pattern |
| `congestion_by_borough.csv` | Borough-level congestion and speed |
| `zone_earnings.csv` | Per-zone effective earnings |

Download these from DBFS and place them in `data/sample/`.

### Deploying to Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect the repo and set **Main file path** to `app.py`
4. Click **Deploy** — no environment variables required
