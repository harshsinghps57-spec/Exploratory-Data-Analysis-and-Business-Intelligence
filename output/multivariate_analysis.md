# Multivariate Analysis & Correlation Report

This report outlines advanced relationships between key columns in the Superstore dataset.

## 1. Key Multivariate Insights

### Discount vs. Profitability Correlation
- The correlation heatmap indicates a **strong negative correlation (-0.70)** between `Discount` and `Profit Margin %`.
- As discount levels rise, profitability declines dramatically. Looking at the boxplot, any discount exceeding 20% (Medium and High groups) results in a median profit margin that is heavily negative (under -50%).

### Product Category Profitability Profile
- Technology items represent the highest high-revenue transactions, with high profits (e.g. imageCLASS Copiers).
- Furniture items, specifically **Tables** and **Bookcases**, exhibit negative profits even when generating high sales revenue. This indicates structural pricing, shipping cost, or discounting issues for bulky furniture categories.

### Sub-Category & Segment Performance
A granular view of profit margins across sub-categories and segments highlights:
- **Highly Profitable combinations:** Paper and Labels are consistently highly profitable (>40% margin) across all Customer Segments (Consumer, Corporate, Home Office).
- **Deeply Loss-making combinations:** Binders in the Consumer segment have a negative average margin due to aggressive discounting. Tables are unprofitable across all three segments (-10% to -18% average margin).

### Operational/Shipping Delay Metrics
- The shipping delay (days) has near-zero correlation with sales value or profit, showing operations remain consistent regardless of order size.
- Same Day shipping successfully delivers within 0-1 days. First Class shipping averages 2 days, Second Class averages 3 days, and Standard Class averages 5 days, consistent across all categories.
