# TLC Dashboard - Data Export Helper
# Run this in your Databricks notebook AFTER tlc_pipeline_clean.ipynb finishes
# Then download the outputs and place them in data/sample/ in the GitHub repo

# ─────────────────────────────────────────────
# 1. Gold layer sample (for fare predictor)
# ─────────────────────────────────────────────
sample = (
    spark.table("tlc_gold.yellow_enriched")
    .sample(fraction=0.005, seed=42)   # ~750K rows — keep GitHub under 100MB
    .select(
        "trip_distance", "trip_duration_mins", "avg_speed_mph",
        "is_airport_trip", "is_rush_hour", "is_post_congestion",
        "is_cbd_pickup", "is_cbd_dropoff", "fare_amount",
        "pickup_hour", "pickup_dow", "pickup_year", "pickup_month",
        "PUBorough", "DOBorough", "route_mean_fare", "distance_ratio",
        "hour_sin", "hour_cos", "dow_sin", "dow_cos",
        "passenger_count", "tip_amount", "total_amount",
    )
    .toPandas()
)

sample.to_parquet("/dbfs/FileStore/tlc_exports/gold_sample.parquet", index=False)
print(f"Exported {len(sample):,} rows → gold_sample.parquet")

# ─────────────────────────────────────────────
# 2. Congestion by year (pre-aggregated CSV)
# ─────────────────────────────────────────────
from pyspark.sql import functions as F

congestion_year = (
    spark.table("tlc_gold.yellow_enriched")
    .groupBy("pickup_year")
    .agg(
        F.avg("congestion_share").alias("congestion_pct"),
        F.avg("fare_amount").alias("avg_fare"),
        (F.sum("trip_duration_mins") / 60 / 1e6).alias("hours_lost_M"),
        F.count("*").alias("trip_count"),
    )
    .orderBy("pickup_year")
    .toPandas()
)
congestion_year["congestion_pct"] = congestion_year["congestion_pct"] * 100
congestion_year.to_csv("/dbfs/FileStore/tlc_exports/congestion_by_year.csv", index=False)
print("Exported congestion_by_year.csv")

# ─────────────────────────────────────────────
# 3. Congestion by hour
# ─────────────────────────────────────────────
congestion_hour = (
    spark.table("tlc_gold.yellow_enriched")
    .groupBy("pickup_hour")
    .agg(F.avg("congestion_share").alias("congestion_pct"))
    .orderBy("pickup_hour")
    .toPandas()
)
congestion_hour["congestion_pct"] = congestion_hour["congestion_pct"] * 100
congestion_hour.to_csv("/dbfs/FileStore/tlc_exports/congestion_by_hour.csv", index=False)
print("Exported congestion_by_hour.csv")

# ─────────────────────────────────────────────
# 4. Congestion by borough
# ─────────────────────────────────────────────
congestion_borough = (
    spark.table("tlc_gold.yellow_enriched")
    .groupBy("PUBorough")
    .agg(
        F.avg("congestion_share").alias("congestion_pct"),
        F.avg("avg_speed_mph").alias("avg_speed_mph"),
        (F.count("*") / 1e6).alias("trips_M"),
    )
    .toPandas()
)
congestion_borough["congestion_pct"] = congestion_borough["congestion_pct"] * 100
congestion_borough.to_csv("/dbfs/FileStore/tlc_exports/congestion_by_borough.csv", index=False)
print("Exported congestion_by_borough.csv")

# ─────────────────────────────────────────────
# 5. Zone earnings
# ─────────────────────────────────────────────
zone_earnings = (
    spark.table("tlc_gold.yellow_enriched")
    .groupBy("PULocationID", "PUBorough")
    .agg(
        F.avg("fare_amount").alias("avg_fare"),
        F.avg("trip_duration_mins").alias("avg_duration_min"),
        F.avg("tip_amount").alias("avg_tip"),
        F.count("*").alias("trip_count"),
    )
    .filter(F.col("trip_count") > 1000)
    .toPandas()
)
# Effective $/hr = avg_fare / (avg_duration_min / 60)
zone_earnings["effective_per_hr"] = (
    zone_earnings["avg_fare"] / (zone_earnings["avg_duration_min"] / 60)
).round(2)
zone_earnings.to_csv("/dbfs/FileStore/tlc_exports/zone_earnings.csv", index=False)
print("Exported zone_earnings.csv")

# ─────────────────────────────────────────────
# Download from DBFS → local
# ─────────────────────────────────────────────
print("\nDownload files from:")
print("  https://<your-workspace>.azuredatabricks.net/files/tlc_exports/gold_sample.parquet")
print("  https://<your-workspace>.azuredatabricks.net/files/tlc_exports/congestion_by_year.csv")
print("  https://<your-workspace>.azuredatabricks.net/files/tlc_exports/congestion_by_hour.csv")
print("  https://<your-workspace>.azuredatabricks.net/files/tlc_exports/congestion_by_borough.csv")
print("  https://<your-workspace>.azuredatabricks.net/files/tlc_exports/zone_earnings.csv")
print("\nOr use: dbutils.fs.cp('dbfs:/FileStore/tlc_exports/', 'file:/home/...', recurse=True)")
