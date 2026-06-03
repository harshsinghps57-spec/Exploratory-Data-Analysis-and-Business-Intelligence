# 📊 Exploratory Data Analysis & Business Intelligence — Week 2 Internship Task

> **ApexPlanet Software Pvt. Ltd. | Internship Task 2 | Timeline: 14 Days**

---

## 📌 Project Overview

This repository contains the deliverables for the **Week 2 Internship Task: Exploratory Data Analysis (EDA) & Business Intelligence**. Using the cleaned dataset generated in Week 1, we executed an in-depth univariate, multivariate, and SQL-based analysis to profile transactions, identify leakage points, and model a high-performance executive dashboard.

---

## 📂 Repository Structure

```
Exploratory-Data-Analysis-and-Business-Intelligence/
│
├── data/
│   ├── Sample - Superstore.csv       # Raw transaction dataset
│   ├── cleaned_superstore.csv        # Week 1 prepared dataset
│   └── superstore.db                 # Normalized SQLite database
│
├── src/
│   ├── univariate_analysis.py        # Descriptive statistics & distribution script
│   ├── multivariate_analysis.py      # Core correlation and advanced visualization script
│   ├── sql_analysis.py               # SQL Database Setup & Queries executor
│   └── generate_dashboard_data.py    # Pre-calculates segment-filtered JSON data
│
├── output/
│   ├── descriptive_statistics.md     # Summary statistics report
│   ├── sql_results.md                # SQL business query results
│   ├── multivariate_analysis.md      # Advanced correlation findings
│   └── charts/                       # Folder containing generated plots
│       ├── sales_profit_distributions.png
│       ├── delay_margin_distributions.png
│       ├── correlation_heatmap.png
│       ├── sales_vs_profit_scatter.png
│       ├── discount_vs_margin_boxplot.png
│       ├── ship_delay_by_mode.png
│       └── margin_heatmap_segment_subcategory.png
│
├── dashboard/
│   ├── index.html                    # Interactive dark-mode BI dashboard
│   ├── data.js                       # Pre-aggregated dataset for filtering
│   └── dashboard_mockup.md           # Dashboard KPI specifications & wireframe
│
└── README.md                         # Project documentation (This file)
```

---

## 🛠️ Installation & Execution

### 1. Prerequisites
Ensure Python 3.x is installed along with the required libraries:
```bash
pip install pandas numpy matplotlib seaborn tabulate openpyxl
```

### 2. Generate Reports and Charts
You can run each script in the `src/` directory to re-generate the outputs:
```bash
# Perform descriptive and univariate analysis
python src/univariate_analysis.py

# Initialize SQLite database and run business SQL queries
python src/sql_analysis.py

# Perform correlation and multivariate analysis
python src/multivariate_analysis.py

# Pre-aggregate data for the interactive dashboard
python src/generate_dashboard_data.py
```

### 3. Open the BI Dashboard
To launch the interactive dashboard, simply open `dashboard/index.html` in any web browser. 
- You can filter the KPIs and charts dynamically by clicking on **Customer Segments** (Consumer, Corporate, Home Office) or **Sales Regions** (East, West, Central, South) at the top of the interface.

---

## 🔑 Critical Business Intelligence Findings

### 1. The Discount Threat Threshold
Our SQL and multivariate analysis identifies **discounts exceeding 20%** as the primary driver of profit loss:
- Transactions with **No Discount** maintain an excellent **29.5% average profit margin**.
- Transactions with **Low Discount (1-20%)** maintain a healthy **11.9% average profit margin**.
- Transactions with **High Discount (>20%)** collapse to a **-37.3% margin**, generating **$135,376 in net losses**.
- *Recommendation:* Restrict standard discount limits to a maximum of 20% in CRM.

### 2. Category Profit Bleed
- **Furniture** generates high sales revenue ($742K) but only **$18,451 in net profit** (a marginal **2.48%** margin).
- **Tables** is the single most loss-making sub-category, generating **-$32,412 in losses**, followed by **Binders** at **-$38,510** due to massive 70%+ promotional discounts.
- *Recommendation:* Re-evaluate the pricing model for heavy furniture items and apply delivery surcharges to cover high shipping logistics costs.

### 3. Star Performers
- **Technology** (especially Copiers and Phones) maintains the highest absolute sales and profit margins.
- **Paper** and **Labels** are highly profitable (margins >40%) across all segments and regions, presenting low-risk expansion opportunities.

---

## 👤 Author

**Harsh Singh**  
Intern @ ApexPlanet Software Pvt. Ltd.  
[GitHub Profile](https://github.com/harshsinghps57-spec)
