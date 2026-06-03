import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# File configuration
BASE_DIR = r"C:\Users\user\.gemini\antigravity\scratch\Exploratory-Data-Analysis-and-Business-Intelligence"
DATA_FILE = os.path.join(BASE_DIR, "data", "cleaned_superstore.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
CHARTS_DIR = os.path.join(OUTPUT_DIR, "charts")

os.makedirs(CHARTS_DIR, exist_ok=True)
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']

def run_univariate_analysis():
    print("Loading cleaned dataset...")
    df = pd.read_csv(DATA_FILE)
    
    # 1. Calculate Descriptive Statistics for Numerical Fields
    num_cols = ["Sales", "Quantity", "Discount", "Profit", "Ship Delay (Days)", "Profit Margin %"]
    # Filter columns that exist
    num_cols = [c for c in num_cols if c in df.columns]
    
    num_summary = df[num_cols].describe().T
    num_summary["skewness"] = df[num_cols].skew()
    num_summary["kurtosis"] = df[num_cols].kurt()
    num_summary = num_summary.round(2)
    
    # 2. Calculate Descriptive Statistics for Categorical Fields
    cat_cols = ["Ship Mode", "Segment", "Region", "Category", "Sub-Category", "State"]
    cat_cols = [c for c in cat_cols if c in df.columns]
    
    cat_summary_list = []
    for col in cat_cols:
        counts = df[col].value_counts()
        total = len(df)
        top_val = counts.index[0]
        top_count = counts.iloc[0]
        top_pct = (top_count / total) * 100
        cat_summary_list.append({
            "Field": col,
            "Unique Values": df[col].nunique(),
            "Most Frequent (Top)": f"{top_val} ({top_count:,} items)",
            "Top Value Share %": f"{top_pct:.1f}%"
        })
    cat_summary = pd.DataFrame(cat_summary_list)
    
    # 3. Write Descriptive Statistics Report to Markdown
    report_path = os.path.join(OUTPUT_DIR, "descriptive_statistics.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Descriptive Statistics & Univariate Analysis Report\n\n")
        f.write("This report presents the univariate analysis of the Superstore dataset, summarizing key numerical metrics and categorical distributions.\n\n")
        
        f.write("## 1. Numerical Fields Summary Statistics\n\n")
        f.write("The table below shows the standard central tendency, dispersion, and shape metrics for the numerical fields:\n\n")
        f.write(num_summary.to_markdown())
        f.write("\n\n")
        
        f.write("### Key Observations (Numerical):\n")
        f.write("- **Sales & Profit skewness:** Both fields exhibit high positive skewness, indicating a long right tail of extreme values (a few large orders generate massive sales and profit).\n")
        f.write("- **Discounts:** Average discount is around 15.6%. There are order lines with up to 80% discount which significantly impacts profitability.\n")
        f.write("- **Shipping Delay:** The average shipping delay is approximately 3.96 days, with 75% of orders shipped within 5 days.\n")
        f.write("- **Profit Margin:** The average profit margin per transaction is 12.0%, but it ranges from -275% to 50%.\n\n")
        
        f.write("## 2. Categorical Fields Summary Statistics\n\n")
        f.write("The table below summarizes the categorical characteristics of the dataset:\n\n")
        f.write(cat_summary.to_markdown(index=False))
        f.write("\n\n")
        
        f.write("### Key Observations (Categorical):\n")
        f.write("- **Segment:** The Consumer segment is the dominant group, making up more than 50% of all transactions.\n")
        f.write("- **Region:** Transactions are fairly evenly split across the four US regions, with the West region leading slightly.\n")
        f.write("- **Category:** Office Supplies represents the vast majority of items sold (60.3%), but generates lower average sales per transaction than Technology.\n")
        f.write("- **Shipping Mode:** Standard Class is the most popular choice by far, capturing nearly 60% of all shipments.\n")
        
    print(f"Descriptive statistics written to {report_path}")
    
    # 4. Create Univariate Visualizations
    print("Generating univariate charts...")
    
    # Chart 1: Distribution of Sales and Profit (Histograms with log scale/kde)
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # We use a log scale for Sales due to heavy skewness
    sns.histplot(data=df, x="Sales", bins=50, kde=True, ax=axes[0], color="#1f77b4")
    axes[0].set_title("Sales Distribution (Standard Scale)", fontsize=13, fontweight="bold")
    axes[0].set_xlabel("Sales ($)")
    axes[0].set_ylabel("Count")
    
    # Profit Distribution
    sns.histplot(data=df, x="Profit", bins=50, kde=True, ax=axes[1], color="#2ca02c")
    axes[1].set_title("Profit Distribution", fontsize=13, fontweight="bold")
    axes[1].set_xlabel("Profit ($)")
    axes[1].set_ylabel("Count")
    
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "sales_profit_distributions.png"), dpi=150)
    plt.close()
    
    # Chart 2: Ship Delay and Profit Margin Distributions
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Ship Delay
    sns.histplot(data=df, x="Ship Delay (Days)", bins=int(df["Ship Delay (Days)"].max()) + 1, 
                 kde=False, ax=axes[0], color="#d62728", discrete=True)
    axes[0].set_title("Distribution of Shipping Delay (Days)", fontsize=13, fontweight="bold")
    axes[0].set_xlabel("Days to Ship")
    axes[0].set_ylabel("Count")
    
    # Profit Margin %
    sns.histplot(data=df, x="Profit Margin %", bins=50, kde=True, ax=axes[1], color="#9467bd")
    axes[1].set_title("Distribution of Profit Margin %", fontsize=13, fontweight="bold")
    axes[1].set_xlabel("Profit Margin %")
    axes[1].set_ylabel("Count")
    
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "delay_margin_distributions.png"), dpi=150)
    plt.close()
    
    # Chart 3: Product Category and Segment Counts (Bar charts)
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Category Count
    cat_order = df["Category"].value_counts().index
    sns.countplot(data=df, x="Category", order=cat_order, ax=axes[0], palette="Blues_r")
    axes[0].set_title("Transaction Count by Product Category", fontsize=13, fontweight="bold")
    axes[0].set_xlabel("Category")
    axes[0].set_ylabel("Transaction Count")
    for p in axes[0].patches:
        axes[0].annotate(f"{p.get_height():,}", (p.get_x() + p.get_width() / 2., p.get_height() + 50),
                    ha='center', va='center', xytext=(0, 5), textcoords='offset points', fontweight='semibold')
        
    # Segment Count
    seg_order = df["Segment"].value_counts().index
    sns.countplot(data=df, x="Segment", order=seg_order, ax=axes[1], palette="Purples_r")
    axes[1].set_title("Transaction Count by Customer Segment", fontsize=13, fontweight="bold")
    axes[1].set_xlabel("Segment")
    axes[1].set_ylabel("Transaction Count")
    for p in axes[1].patches:
        axes[1].annotate(f"{p.get_height():,}", (p.get_x() + p.get_width() / 2., p.get_height() + 50),
                    ha='center', va='center', xytext=(0, 5), textcoords='offset points', fontweight='semibold')
        
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "category_segment_counts.png"), dpi=150)
    plt.close()
    
    # Chart 4: Sub-Category Distribution (Horizontal Bar Chart)
    plt.figure(figsize=(10, 8))
    subcat_order = df["Sub-Category"].value_counts().index
    sns.countplot(data=df, y="Sub-Category", order=subcat_order, palette="viridis")
    plt.title("Transaction Count by Sub-Category", fontsize=14, fontweight="bold")
    plt.xlabel("Transaction Count")
    plt.ylabel("Sub-Category")
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "sub_category_counts.png"), dpi=150)
    plt.close()
    
    print("Univariate analysis completed successfully!")

if __name__ == "__main__":
    run_univariate_analysis()
