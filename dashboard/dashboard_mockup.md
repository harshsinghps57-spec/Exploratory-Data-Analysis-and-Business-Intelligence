# Business Intelligence Dashboard Proposal & Mock-up Design

This document details the proposal and structural design of the key metrics dashboard for Superstore Management. It proposes the key metrics, targets, layouts, and recommendations derived from our Exploratory Data Analysis.

An interactive static mock-up implementation is available at [dashboard/index.html](file:///C:/Users/user/.gemini/antigravity/scratch/Exploratory-Data-Analysis-and-Business-Intelligence/dashboard/index.html).

---

## 📈 Proposed Key Performance Indicators (KPIs)

To drive profitability and operational health, the dashboard tracks four primary KPIs:

| KPI Name | Business Definition & Formula | Current Value | Target / Benchmark | Actionable Owner |
| :--- | :--- | :--- | :--- | :--- |
| **Total Revenue (Sales)** | Sum of transaction sales prices: `SUM(sales)` | **$2,297,201** | Maintain > 15% YoY growth | Sales & Marketing VP |
| **Total Operating Profit** | Sum of line profits/losses: `SUM(profit)` | **$286,397** | Increase margin share | Operations VP |
| **Operating Profit Margin %** | Profit efficiency: `(SUM(profit) / SUM(sales)) * 100` | **12.47%** | Target **> 15.0%** margin | Finance & Pricing VP |
| **Avg Shipping Delay** | Operations speed: `AVG(ship_date - order_date)` | **3.96 Days** | Target **< 4.0 Days** | Logistics Director |

---

## 🖼️ Dashboard Wireframe & Layout Design

The dashboard is structured using a modern grid layout designed for cognitive flow:

```
+------------------------------------------------------------------------------------+
|  [Logo] APEXPLANET BI DASHBOARD                       [Filter: Segment] [Filter: Region] |
+------------------------------------------------------------------------------------+
|  💡 Executive Insight Alert: Pricing Leakage Identified (e.g. Binders, Tables losses) |
+------------------------------------------------------------------------------------+
|  +---------------------+ +---------------------+ +---------------------+ +---------------------+  |
|  | TOTAL REVENUE       | | TOTAL NET PROFIT    | | PROFIT MARGIN %     | | AVG SHIP DELAY      |  |
|  | $2,297,201          | | $286,397            | | 12.47%              | | 3.96 Days           |  |
|  | (Dynamic trend indicator)                   | | (Dynamic status indicator)                |  |
|  +---------------------+ +---------------------+ +---------------------+ +---------------------+  |
+------------------------------------------------------------------------------------+
|  +--------------------------------------------+ +----------------------------------+  |
|  | CHART 1: Monthly Sales & Profit Trend      | | CHART 2: Profit Margin %         |  |
|  | (Interactive Line / Area Chart)            | | by Discount Band (Bar Chart)     |  |
|  |                                            | | No Disc (29.5%) | Low (11.9%) |   |
|  |                                            | | High Disc (-37.3% [LOSS])        |  |
|  +--------------------------------------------+ +----------------------------------+  |
+------------------------------------------------------------------------------------+
|  +--------------------------------------------+ +----------------------------------+  |
|  | CHART 3: Sales & Profit by Category        | | CHART 4: Sub-Category Loss      |  |
|  | (Grouped Bar Chart - Tech, Office, Furn)   | | Leaders (Horizontal Bar Chart)   |  |
|  |                                            | | Binders ($38K Loss)              |  |
|  |                                            | | Tables ($32K Loss)               |  |
|  +--------------------------------------------+ +----------------------------------+  |
+------------------------------------------------------------------------------------+
```

---

## 🔍 Core EDA-Driven Insights for Board Review

### 1. The Discount Threshold Trap (Pricing Leakage)
Our bivariate analysis reveals a critical profit inflection point:
- Transactions with **No Discount** maintain an excellent **29.5% profit margin**.
- Transactions with **Low Discount (1-20%)** yield a **11.9% profit margin**.
- Transactions with **High Discount (>20%)** collapse to a **-37.3% margin**, generating **$135,376 in net losses**.
- **Actionable Recommendation:** Implement an automated hard ceiling on discounts at 20% in the CRM. Any discount above 20% must require executive director approval.

### 2. Bulky Logistics Bleed (Furniture)
- Product Category analysis shows **Furniture** represents $742,000 in sales but only **$18,451 in net profit** (an operating margin of **2.48%**).
- **Tables** (Furniture) generated **-$32,412 in losses**.
- **Actionable Recommendation:** Revise shipping cost allocations for heavy items. Charge shipping premiums for bulky furniture orders rather than absorbing costs in flat standard delivery fees.
