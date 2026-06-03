import os
import sqlite3
import pandas as pd
import numpy as np

# File configuration
BASE_DIR = r"C:\Users\user\.gemini\antigravity\scratch\Exploratory-Data-Analysis-and-Business-Intelligence"
DATA_FILE = os.path.join(BASE_DIR, "data", "cleaned_superstore.csv")
DB_FILE = os.path.join(BASE_DIR, "data", "superstore.db")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

os.makedirs(OUTPUT_DIR, exist_ok=True)

def setup_database():
    print("Setting up SQLite database...")
    df = pd.read_csv(DATA_FILE)
    
    # Clean and rename all CSV columns to lowercase snake_case
    df.rename(columns={
        "Row ID": "row_id",
        "Order ID": "order_id",
        "Order Date": "order_date",
        "Ship Date": "ship_date",
        "Ship Mode": "ship_mode",
        "Customer ID": "customer_id",
        "Customer Name": "customer_name",
        "Segment": "segment",
        "Country": "country",
        "City": "city",
        "State": "state",
        "Postal Code": "postal_code",
        "Region": "region",
        "Product ID": "product_id",
        "Category": "category",
        "Sub-Category": "sub_category",
        "Product Name": "product_name",
        "Sales": "sales",
        "Quantity": "quantity",
        "Discount": "discount",
        "Profit": "profit",
        "Order Year": "order_year",
        "Order Month": "order_month",
        "Order Quarter": "order_quarter",
        "Ship Delay (Days)": "ship_delay_days",
        "Profit Margin %": "profit_margin_pct",
        "Sales Outlier Flag": "sales_outlier_flag"
    }, inplace=True)
    
    # Preprocess dates to standard ISO strings for SQLite
    df["order_date"] = pd.to_datetime(df["order_date"]).dt.strftime("%Y-%m-%d")
    df["ship_date"] = pd.to_datetime(df["ship_date"]).dt.strftime("%Y-%m-%d")
    
    # 1. Normalize into Customers Table
    customers = df[["customer_id", "customer_name", "segment"]].drop_duplicates(subset=["customer_id"])
    
    # 2. Normalize into Locations Table
    # Fill missing postal codes with 0 for ID purposes
    df["postal_code"] = df["postal_code"].fillna(0).astype(int)
    locations = df[["postal_code", "city", "state", "country", "region"]].drop_duplicates(subset=["postal_code", "city", "state"])
    # Generate unique location_id
    locations = locations.reset_index(drop=True)
    locations["location_id"] = locations.index + 1
    
    # Map location_id back to df
    df = df.merge(locations, on=["postal_code", "city", "state", "country", "region"], how="left")
    
    # 3. Normalize into Products Table
    products = df[["product_id", "product_name", "category", "sub_category"]].drop_duplicates(subset=["product_id"])
    
    # 4. Normalize into Orders Table
    orders = df[["order_id", "order_date", "ship_date", "ship_mode", "customer_id", "location_id"]].drop_duplicates(subset=["order_id"])
    
    # 5. Normalize into Order Items Table
    order_items = df[[
        "row_id", "order_id", "product_id", "sales", "quantity", 
        "discount", "profit", "ship_delay_days", "profit_margin_pct", "sales_outlier_flag"
    ]].copy()
    
    # Clean up locations columns for export
    locations = locations[["location_id", "postal_code", "city", "state", "country", "region"]]
    
    # Save to SQLite
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        
    conn = sqlite3.connect(DB_FILE)
    
    customers.to_sql("customers", conn, index=False, if_exists="replace")
    locations.to_sql("locations", conn, index=False, if_exists="replace")
    products.to_sql("products", conn, index=False, if_exists="replace")
    orders.to_sql("orders", conn, index=False, if_exists="replace")
    order_items.to_sql("order_items", conn, index=False, if_exists="replace")
    
    conn.close()
    print(f"Database successfully created at {DB_FILE} with normalized schema.")

def execute_queries_and_report():
    conn = sqlite3.connect(DB_FILE)
    
    report_path = os.path.join(OUTPUT_DIR, "sql_results.md")
    
    # Helper function to run query and return markdown and dataframe
    def run_query(title, query, desc):
        print(f"Running query: {title}")
        df_res = pd.read_sql_query(query, conn)
        md = f"### {title}\n\n"
        md += f"**Description:** {desc}\n\n"
        md += "**SQL Query:**\n```sql\n" + query.strip() + "\n```\n\n"
        md += "**Results:**\n\n"
        md += df_res.to_markdown(index=False)
        md += "\n\n"
        return md

    queries_md = ""
    
    # Query 1: Top 5 Products by Revenue in Last 6 Months
    q1_desc = "Find the top 5 products by revenue in the last 6 months of the dataset. First, we find the maximum date in the orders table, subtract 6 months, and join tables to compute total sales per product."
    q1 = """
WITH DateLimit AS (
    SELECT date(max(order_date), '-6 months') AS six_months_ago
    FROM orders
)
SELECT 
    p.product_id AS [Product ID],
    p.product_name AS [Product Name],
    p.category AS [Category],
    ROUND(SUM(oi.sales), 2) AS [Total Revenue ($)],
    SUM(oi.quantity) AS [Total Quantity Sold]
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_date >= (SELECT six_months_ago FROM DateLimit)
GROUP BY p.product_id, p.product_name, p.category
ORDER BY [Total Revenue ($)] DESC
LIMIT 5;
"""
    queries_md += run_query("1. Top 5 Products by Revenue (Last 6 Months)", q1, q1_desc)
    
    # Query 2: Customer Acquisition Trend
    q2_desc = "Compute the monthly user acquisition trend. A user is 'acquired' on the date of their very first order. We identify each customer's first order date and aggregate counts by year and month."
    q2 = """
WITH CustomerFirstOrder AS (
    SELECT 
        customer_id,
        MIN(order_date) AS first_order_date
    FROM orders
    GROUP BY customer_id
),
AcquisitionByMonth AS (
    SELECT 
        strftime('%Y-%m', first_order_date) AS YearMonth,
        COUNT(customer_id) AS NewCustomersCount
    FROM CustomerFirstOrder
    GROUP BY YearMonth
)
SELECT 
    YearMonth AS [Year-Month],
    NewCustomersCount AS [New Customers Acquired]
FROM AcquisitionByMonth
ORDER BY [Year-Month] ASC
LIMIT 12; -- showing first 12 months for brevity in report
"""
    queries_md += run_query("2. Monthly Customer Acquisition Trend (First 12 Months)", q2, q2_desc)

    # Query 3: Profit Margin by Region and Customer Segment
    q3_desc = "Compute the total sales, total profit, and weighted profit margin % grouped by geographic region and customer segment. This query joins four normalized tables: order_items, orders, customers, and locations."
    q3 = """
SELECT 
    l.region AS [Region],
    c.segment AS [Customer Segment],
    ROUND(SUM(oi.sales), 2) AS [Total Sales ($)],
    ROUND(SUM(oi.profit), 2) AS [Total Profit ($)],
    ROUND((SUM(oi.profit) / SUM(oi.sales)) * 100, 2) AS [Profit Margin %]
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
JOIN customers c ON o.customer_id = c.customer_id
JOIN locations l ON o.location_id = l.location_id
GROUP BY l.region, c.segment
ORDER BY l.region ASC, [Profit Margin %] DESC;
"""
    queries_md += run_query("3. Sales and Profitability by Region and Segment", q3, q3_desc)

    # Query 4: Discount Impact on Profitability
    q4_desc = "Examine the impact of discount levels on sales volume, profit, and margin. Transactions are grouped into three discount bands: No Discount (0%), Low Discount (0.1% to 20%), and High Discount (more than 20%)."
    q4 = """
SELECT 
    CASE 
        WHEN discount = 0 THEN 'No Discount (0%)'
        WHEN discount > 0 AND discount <= 0.2 THEN 'Low Discount (1% - 20%)'
        ELSE 'High Discount (>20%)'
    END AS [Discount Band],
    COUNT(row_id) AS [Transaction Count],
    ROUND(SUM(sales), 2) AS [Total Sales ($)],
    ROUND(SUM(profit), 2) AS [Total Profit ($)],
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS [Profit Margin %],
    ROUND(AVG(ship_delay_days), 2) AS [Avg Ship Delay (Days)]
FROM order_items
GROUP BY [Discount Band]
ORDER BY [Profit Margin %] DESC;
"""
    queries_md += run_query("4. Discount Impact Analysis", q4, q4_desc)

    # Query 5: High-Value Customer Retention
    q5_desc = "Identify the top 10 customers by total sales, showing their segment, total amount spent, number of unique orders placed, and average order value."
    q5 = """
SELECT 
    c.customer_id AS [Customer ID],
    c.customer_name AS [Customer Name],
    c.segment AS [Segment],
    ROUND(SUM(oi.sales), 2) AS [Total Spent ($)],
    COUNT(DISTINCT o.order_id) AS [Total Orders],
    ROUND(SUM(oi.sales) / COUNT(DISTINCT o.order_id), 2) AS [Avg Order Value ($)]
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.customer_name, c.segment
ORDER BY [Total Spent ($)] DESC
LIMIT 10;
"""
    queries_md += run_query("5. Top 10 Customers by Sales and Order Volume", q5, q5_desc)

    # Query 6: Highly Unprofitable Products
    q6_desc = "Analyze product sub-categories to identify where the highest losses are generated. This query filters for negative-profit transactions and aggregates the loss amount and count of loss-making items."
    q6 = """
SELECT 
    p.sub_category AS [Sub-Category],
    p.category AS [Category],
    ROUND(SUM(oi.profit), 2) AS [Total Losses ($)],
    COUNT(oi.row_id) AS [Number of Unprofitable Transactions],
    ROUND(AVG(oi.discount) * 100, 1) AS [Avg Discount Offered %]
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
WHERE oi.profit < 0
GROUP BY p.sub_category, p.category
ORDER BY [Total Losses ($)] ASC;
"""
    queries_md += run_query("6. Losses and Unprofitability by Sub-Category", q6, q6_desc)

    # Write SQL Report to File
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# SQL Business Intelligence Analysis Report\n\n")
        f.write("This report presents SQL queries and matching result tables that extract critical business insights from the Superstore database. ")
        f.write("To simulate a realistic database environment, the raw flat dataset was normalized into 5 tables: `customers`, `locations`, `products`, `orders`, and `order_items` inside a SQLite database.\n\n")
        f.write("## Database Normalized Schema Description\n")
        f.write("- **`customers`**: Unique customers by `customer_id` (contains customer names and segments).\n")
        f.write("- **`locations`**: Unique locations by `location_id` (contains cities, states, postal codes, and regions).\n")
        f.write("- **`products`**: Unique products by `product_id` (contains product names, categories, and sub-categories).\n")
        f.write("- **`orders`**: Unique orders by `order_id` (contains order/ship dates, shipping modes, customer IDs, and location IDs).\n")
        f.write("- **`order_items`**: Line item sales details with foreign keys linking back to orders and products.\n\n")
        f.write("## Business Query Results\n\n")
        f.write(queries_md)
        
    conn.close()
    print(f"SQL analysis results written to {report_path}")

if __name__ == "__main__":
    setup_database()
    execute_queries_and_report()
