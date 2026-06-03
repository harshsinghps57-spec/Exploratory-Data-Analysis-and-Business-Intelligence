# Descriptive Statistics & Univariate Analysis Report

This report presents the univariate analysis of the Superstore dataset, summarizing key numerical metrics and categorical distributions.

## 1. Numerical Fields Summary Statistics

The table below shows the standard central tendency, dispersion, and shape metrics for the numerical fields:

|                   |   count |   mean |    std |      min |   25% |   50% |    75% |      max |   skewness |   kurtosis |
|:------------------|--------:|-------:|-------:|---------:|------:|------:|-------:|---------:|-----------:|-----------:|
| Sales             |    9994 | 229.86 | 623.25 |     0.44 | 17.28 | 54.49 | 209.94 | 22638.5  |      12.97 |     305.31 |
| Quantity          |    9994 |   3.79 |   2.23 |     1    |  2    |  3    |   5    |    14    |       1.28 |       1.99 |
| Discount          |    9994 |   0.16 |   0.21 |     0    |  0    |  0.2  |   0.2  |     0.8  |       1.68 |       2.41 |
| Profit            |    9994 |  28.66 | 234.26 | -6599.98 |  1.73 |  8.67 |  29.36 |  8399.98 |       7.56 |     397.19 |
| Ship Delay (Days) |    9994 |   3.96 |   1.75 |     0    |  3    |  4    |   5    |     7    |      -0.42 |      -0.29 |
| Profit Margin %   |    9994 |  12.03 |  46.68 |  -275    |  7.5  | 27    |  36.25 |    50    |      -2.89 |      10.17 |

### Key Observations (Numerical):
- **Sales & Profit skewness:** Both fields exhibit high positive skewness, indicating a long right tail of extreme values (a few large orders generate massive sales and profit).
- **Discounts:** Average discount is around 15.6%. There are order lines with up to 80% discount which significantly impacts profitability.
- **Shipping Delay:** The average shipping delay is approximately 3.96 days, with 75% of orders shipped within 5 days.
- **Profit Margin:** The average profit margin per transaction is 12.0%, but it ranges from -275% to 50%.

## 2. Categorical Fields Summary Statistics

The table below summarizes the categorical characteristics of the dataset:

| Field        |   Unique Values | Most Frequent (Top)           | Top Value Share %   |
|:-------------|----------------:|:------------------------------|:--------------------|
| Ship Mode    |               4 | Standard Class (5,968 items)  | 59.7%               |
| Segment      |               3 | Consumer (5,191 items)        | 51.9%               |
| Region       |               4 | West (3,203 items)            | 32.0%               |
| Category     |               3 | Office Supplies (6,026 items) | 60.3%               |
| Sub-Category |              17 | Binders (1,523 items)         | 15.2%               |
| State        |              49 | California (2,001 items)      | 20.0%               |

### Key Observations (Categorical):
- **Segment:** The Consumer segment is the dominant group, making up more than 50% of all transactions.
- **Region:** Transactions are fairly evenly split across the four US regions, with the West region leading slightly.
- **Category:** Office Supplies represents the vast majority of items sold (60.3%), but generates lower average sales per transaction than Technology.
- **Shipping Mode:** Standard Class is the most popular choice by far, capturing nearly 60% of all shipments.
