import os
import json
import pandas as pd
import numpy as np

# File configuration
BASE_DIR = r"C:\Users\user\.gemini\antigravity\scratch\Exploratory-Data-Analysis-and-Business-Intelligence"
DATA_FILE = os.path.join(BASE_DIR, "data", "cleaned_superstore.csv")
DASHBOARD_DIR = os.path.join(BASE_DIR, "dashboard")
DATA_JS_FILE = os.path.join(DASHBOARD_DIR, "data.js")

os.makedirs(DASHBOARD_DIR, exist_ok=True)

def generate_data():
    print("Generating dashboard dataset...")
    df = pd.read_csv(DATA_FILE)
    
    # Standardize column names
    df.rename(columns={
        "Sales": "sales",
        "Quantity": "quantity",
        "Discount": "discount",
        "Profit": "profit",
        "Ship Delay (Days)": "ship_delay_days",
        "Profit Margin %": "profit_margin_pct",
        "Category": "category",
        "Sub-Category": "sub_category",
        "Segment": "segment",
        "Region": "region",
        "Ship Mode": "ship_mode",
        "Order Date": "order_date"
    }, inplace=True)
    
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["year_month"] = df["order_date"].dt.strftime("%Y-%m")
    
    # We want to support filtering by:
    # 1. Segment (All, Consumer, Corporate, Home Office)
    # 2. Region (All, Central, East, South, West)
    
    data = {}
    
    def get_metrics(sub_df):
        total_sales = float(sub_df["sales"].sum())
        total_profit = float(sub_df["profit"].sum())
        avg_margin = float((total_profit / total_sales * 100) if total_sales > 0 else 0)
        avg_delay = float(sub_df["ship_delay_days"].mean())
        transaction_count = int(len(sub_df))
        
        # Monthly trends (Sorted chronologically)
        monthly = sub_df.groupby("year_month").agg(
            sales=("sales", "sum"),
            profit=("profit", "sum")
        ).reset_index().sort_values("year_month")
        
        monthly_trends = {
            "labels": monthly["year_month"].tolist(),
            "sales": monthly["sales"].round(2).tolist(),
            "profit": monthly["profit"].round(2).tolist()
        }
        
        # Category Breakdown
        category = sub_df.groupby("category").agg(
            sales=("sales", "sum"),
            profit=("profit", "sum")
        ).reset_index()
        
        category_breakdown = {
            "labels": category["category"].tolist(),
            "sales": category["sales"].round(2).tolist(),
            "profit": category["profit"].round(2).tolist()
        }
        
        # Sub-Category Profitability (Top losses)
        sub_loss = sub_df[sub_df["profit"] < 0].groupby("sub_category")["profit"].sum().reset_index()
        sub_loss = sub_loss.sort_values("profit", ascending=True).head(5)  # Most negative profit
        
        sub_loss_breakdown = {
            "labels": sub_loss["sub_category"].tolist(),
            "losses": (-sub_loss["profit"]).round(2).tolist() # Positive loss value for bar chart
        }
        
        # Discount impact bands
        discount_bands = []
        bands = [
            ("No Discount (0%)", sub_df[sub_df["discount"] == 0]),
            ("Low (1-20%)", sub_df[(sub_df["discount"] > 0) & (sub_df["discount"] <= 0.2)]),
            ("High (>20%)", sub_df[sub_df["discount"] > 0.2])
        ]
        for name, band_df in bands:
            band_sales = float(band_df["sales"].sum())
            band_profit = float(band_df["profit"].sum())
            band_margin = float((band_profit / band_sales * 100) if band_sales > 0 else 0)
            discount_bands.append({
                "band": name,
                "count": int(len(band_df)),
                "sales": round(band_sales, 2),
                "profit": round(band_profit, 2),
                "margin": round(band_margin, 2)
            })
            
        return {
            "kpi": {
                "sales": round(total_sales, 2),
                "profit": round(total_profit, 2),
                "margin": round(avg_margin, 2),
                "delay": round(avg_delay, 2),
                "transactions": transaction_count
            },
            "monthly": monthly_trends,
            "category": category_breakdown,
            "sub_loss": sub_loss_breakdown,
            "discounts": discount_bands
        }
    
    # 1. Global (All)
    data["All"] = get_metrics(df)
    
    # 2. Segments
    for seg in df["segment"].unique():
        data[f"segment_{seg}"] = get_metrics(df[df["segment"] == seg])
        
    # 3. Regions
    for reg in df["region"].unique():
        data[f"region_{reg}"] = get_metrics(df[df["region"] == reg])
        
    # Output to data.js
    with open(DATA_JS_FILE, "w", encoding="utf-8") as f:
        f.write("// Pre-calculated data generated from Superstore dataset for Week 2 BI Dashboard\n")
        f.write("const dashboardData = ")
        json.dump(data, f, indent=2)
        f.write(";\n")
        
    print(f"Data generated and written to {DATA_JS_FILE}")

if __name__ == "__main__":
    generate_data()
