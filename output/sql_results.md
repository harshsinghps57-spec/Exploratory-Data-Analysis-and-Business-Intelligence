# SQL Business Intelligence Analysis Report

This report presents SQL queries and matching result tables that extract critical business insights from the Superstore database. To simulate a realistic database environment, the raw flat dataset was normalized into 5 tables: `customers`, `locations`, `products`, `orders`, and `order_items` inside a SQLite database.

## Database Normalized Schema Description
- **`customers`**: Unique customers by `customer_id` (contains customer names and segments).
- **`locations`**: Unique locations by `location_id` (contains cities, states, postal codes, and regions).
- **`products`**: Unique products by `product_id` (contains product names, categories, and sub-categories).
- **`orders`**: Unique orders by `order_id` (contains order/ship dates, shipping modes, customer IDs, and location IDs).
- **`order_items`**: Line item sales details with foreign keys linking back to orders and products.

## Business Query Results

### 1. Top 5 Products by Revenue (Last 6 Months)

**Description:** Find the top 5 products by revenue in the last 6 months of the dataset. First, we find the maximum date in the orders table, subtract 6 months, and join tables to compute total sales per product.

**SQL Query:**
```sql
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
```

**Results:**

| Product ID      | Product Name                                                                | Category        |   Total Revenue ($) |   Total Quantity Sold |
|:----------------|:----------------------------------------------------------------------------|:----------------|--------------------:|----------------------:|
| TEC-CO-10004722 | Canon imageCLASS 2200 Advanced Copier                                       | Technology      |            21699.9  |                     7 |
| OFF-BI-10001359 | GBC DocuBind TL300 Electric Binding System                                  | Office Supplies |             8252.31 |                    16 |
| TEC-MA-10004125 | Cubify CubeX 3D Printer Triple Head Print                                   | Technology      |             7999.98 |                     4 |
| OFF-BI-10003527 | Fellowes PB500 Electric Punch Plastic Comb Binding Machine with Manual Bind | Office Supplies |             7371.74 |                    14 |
| OFF-SU-10002881 | Martin Yale Chadless Opener Electric Letter Opener                          | Office Supplies |             6329.36 |                     9 |

### 2. Monthly Customer Acquisition Trend (First 12 Months)

**Description:** Compute the monthly user acquisition trend. A user is 'acquired' on the date of their very first order. We identify each customer's first order date and aggregate counts by year and month.

**SQL Query:**
```sql
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
```

**Results:**

| Year-Month   |   New Customers Acquired |
|:-------------|-------------------------:|
| 2014-01      |                       32 |
| 2014-02      |                       24 |
| 2014-03      |                       65 |
| 2014-04      |                       56 |
| 2014-05      |                       56 |
| 2014-06      |                       48 |
| 2014-07      |                       44 |
| 2014-08      |                       49 |
| 2014-09      |                       68 |
| 2014-10      |                       42 |
| 2014-11      |                       62 |
| 2014-12      |                       49 |

### 3. Sales and Profitability by Region and Segment

**Description:** Compute the total sales, total profit, and weighted profit margin % grouped by geographic region and customer segment. This query joins four normalized tables: order_items, orders, customers, and locations.

**SQL Query:**
```sql
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
```

**Results:**

| Region   | Customer Segment   |   Total Sales ($) |   Total Profit ($) |   Profit Margin % |
|:---------|:-------------------|------------------:|-------------------:|------------------:|
| Central  | Home Office        |           91212.6 |           12438.4  |             13.64 |
| Central  | Corporate          |          157996   |           18703.9  |             11.84 |
| Central  | Consumer           |          252031   |            8564.05 |              3.4  |
| East     | Home Office        |          127464   |           26709.2  |             20.95 |
| East     | Corporate          |          200409   |           23622.6  |             11.79 |
| East     | Consumer           |          350908   |           41191    |             11.74 |
| South    | Consumer           |          195581   |           26913.6  |             13.76 |
| South    | Corporate          |          121886   |           15215.2  |             12.48 |
| South    | Home Office        |           74255   |            4620.63 |              6.22 |
| West     | Consumer           |          362881   |           57450.6  |             15.83 |
| West     | Corporate          |          225855   |           34437.4  |             15.25 |
| West     | Home Office        |          136722   |           16530.4  |             12.09 |

### 4. Discount Impact Analysis

**Description:** Examine the impact of discount levels on sales volume, profit, and margin. Transactions are grouped into three discount bands: No Discount (0%), Low Discount (0.1% to 20%), and High Discount (more than 20%).

**SQL Query:**
```sql
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
```

**Results:**

| Discount Band           |   Transaction Count |   Total Sales ($) |   Total Profit ($) |   Profit Margin % |   Avg Ship Delay (Days) |
|:------------------------|--------------------:|------------------:|-------------------:|------------------:|------------------------:|
| No Discount (0%)        |                4798 |       1.08791e+06 |             320988 |             29.51 |                    3.99 |
| Low Discount (1% - 20%) |                3803 |  846522           |             100785 |             11.91 |                    3.92 |
| High Discount (>20%)    |                1393 |  362770           |            -135376 |            -37.32 |                    3.96 |

### 5. Top 10 Customers by Sales and Order Volume

**Description:** Identify the top 10 customers by total sales, showing their segment, total amount spent, number of unique orders placed, and average order value.

**SQL Query:**
```sql
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
```

**Results:**

| Customer ID   | Customer Name      | Segment     |   Total Spent ($) |   Total Orders |   Avg Order Value ($) |
|:--------------|:-------------------|:------------|------------------:|---------------:|----------------------:|
| SM-20320      | Sean Miller        | Home Office |           25043   |              5 |               5008.61 |
| TC-20980      | Tamara Chand       | Corporate   |           19052.2 |              5 |               3810.44 |
| RB-19360      | Raymond Buch       | Consumer    |           15117.3 |              6 |               2519.56 |
| TA-21385      | Tom Ashbrook       | Home Office |           14595.6 |              4 |               3648.91 |
| AB-10105      | Adrian Barton      | Consumer    |           14473.6 |             10 |               1447.36 |
| KL-16645      | Ken Lonsdale       | Consumer    |           14175.2 |             12 |               1181.27 |
| SC-20095      | Sanjit Chand       | Consumer    |           14142.3 |              9 |               1571.37 |
| HL-15040      | Hunter Lopez       | Consumer    |           12873.3 |              6 |               2145.55 |
| SE-20110      | Sanjit Engle       | Consumer    |           12209.4 |             11 |               1109.95 |
| CC-12370      | Christopher Conant | Consumer    |           12129.1 |              5 |               2425.81 |

### 6. Losses and Unprofitability by Sub-Category

**Description:** Analyze product sub-categories to identify where the highest losses are generated. This query filters for negative-profit transactions and aggregates the loss amount and count of loss-making items.

**SQL Query:**
```sql
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
```

**Results:**

| Sub-Category   | Category        |   Total Losses ($) |   Number of Unprofitable Transactions |   Avg Discount Offered % |
|:---------------|:----------------|-------------------:|--------------------------------------:|-------------------------:|
| Binders        | Office Supplies |          -38510.5  |                                   613 |                     73.8 |
| Tables         | Furniture       |          -32412.2  |                                   203 |                     36.5 |
| Machines       | Technology      |          -30118.7  |                                    44 |                     58.2 |
| Bookcases      | Furniture       |          -12152.2  |                                   109 |                     34.9 |
| Chairs         | Furniture       |           -9880.84 |                                   235 |                     26.1 |
| Appliances     | Office Supplies |           -8629.64 |                                    67 |                     80   |
| Phones         | Technology      |           -7530.62 |                                   136 |                     34.3 |
| Furnishings    | Furniture       |           -6490.91 |                                   167 |                     53.1 |
| Storage        | Office Supplies |           -6426.3  |                                   161 |                     20   |
| Supplies       | Office Supplies |           -3015.62 |                                    33 |                     20   |
| Accessories    | Technology      |            -930.63 |                                    91 |                     20   |
| Fasteners      | Office Supplies |             -33.2  |                                    12 |                     20   |

