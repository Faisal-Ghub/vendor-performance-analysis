# 🏪 Vendor Performance Analysis — End-to-End Data Analytics Project

An end-to-end data analytics pipeline built to help a retail/wholesale business diagnose vendor inefficiencies, reduce capital lock-up, and maximize profitability across its supply chain.

---

## 📌 Business Problem

Effective inventory and sales management are critical for optimizing profitability in the retail and wholesale industry. Companies need to ensure that they are not incurring losses due to inefficient pricing, poor inventory turnover, or vendor dependency. The goal of this analysis is to:

- Identify underperforming brands that require promotional or pricing adjustments
- Determine top vendors contributing to sales and gross profit
- Analyze the impact of bulk purchasing on unit costs
- Assess inventory turnover to reduce holding costs and improve efficiency
- Investigate the profitability variance between high-performing and low-performing vendors

---


## 📊 Key Business Metrics (Dashboard Highlights)

| Metric | Value |
|---|---|
| 💰 Total Sales | **$441.41M** |
| 🛒 Total Purchase | **$307.34M** |
| 📈 Total Gross Profit | **$134.07M** |
| 🎯 Overall Profit Margin | **38.72%** |
| 📦 Unsold Capital (Locked Inventory) | **$2.71M** |

---

## 💡 Key Insights & Business Impact

### 1. Vendor Concentration Risk
> Top 10 vendors account for **66% of total procurement spend** — a critical concentration risk. Diageo North America Inc alone drives **$68M in sales (16.3% purchase contribution)**, making the business highly dependent on a single supplier.

### 2. Bulk Purchasing Drives Significant Cost Savings
> Unit purchase prices drop dramatically with order volume:

| Order Size | Avg. Unit Price |
|---|---|
| Small | $39.07 |
| Medium | $15.49 |
| Large | $10.78 |

> **Scaling to large orders reduces unit cost by ~72%** compared to small orders — a direct lever for margin improvement.

### 3. Statistically Proven Profit Margin Gap
> A two-sample t-test (t = -17.67, **p ≈ 0.0000**) confirms a statistically significant difference in profit margins between top and low-performing vendors:

| Vendor Segment | Mean Profit Margin | 95% Confidence Interval |
|---|---|---|
| Top Performers | 31.18% | (30.74%, 31.61%) |
| Low Performers | 41.57% | (40.50%, 42.64%) |

> **Counterintuitive finding:** Low-performing vendors (by sales volume) actually have higher profit margins — suggesting untapped revenue potential in vendors that are currently under-promoted.

### 4. Unsold Inventory Capital Lock-up
> **$2.71M is locked in unsold inventory** across vendors — capital that could be redeployed. Vendors with StockTurnover < 1 (sold less than they purchased) were identified as priority targets for inventory optimization.

### 5. Hidden Gems — High Margin, Low Sales Brands
> Using 15th percentile (sales) and 85th percentile (margin) thresholds, specific brands were flagged as underperforming commercially despite strong margins — prime candidates for targeted promotional spend.

---

## Dataset: 

https://drive.google.com/drive/folders/1yvBiZ1MNFTrJWgeoY53eLVlOKnxcOBDe

Due to GitHub file size limitations, the dataset is hosted externally also.

--- 


## 🗂️ Project Structure

```
vendor-performance-analysis/
│
├── dashboard/                         # Power BI dashboard file
│          
├── Data/                              # Raw source data (6 CSV files)
│   ├── begin_inventory.csv
│   ├── end_inventory.csv
│   ├── purchase_prices.csv           # Other csv files are stored in drive (scroll down to access the link)
│
├── images/
│    ├── dashboard/ CI/ Unit Pirce/ Heatmap
│
├── notebooks/
│   ├── Exploratory_Data_Analysis.ipynb        # Data validation & summary pipeline
│   └── Vendor_Performance_Analysis.ipynb      # Full analysis & statistical testing
│
├── ingestion_db.py                    # Chunked CSV ingestion into SQLite (100K rows/chunk)
├── get_vendor_summary.py              # SQL aggregation + feature engineering + DB ingest
├── vendor_sales_summary.xlsx          # Final clean dataset exported for Power BI
│
└── README.md
```

---

## 🔧 Tech Stack

| Layer | Tools |
|---|---|
| Data Ingestion | Python, pandas, SQLAlchemy, SQLite |
| Data Storage | SQLite (`inventory.db`) |
| Data Processing | pandas, NumPy |
| Statistical Analysis | SciPy (`ttest_ind`, confidence intervals) |
| Visualization (EDA) | Matplotlib, Seaborn |
| Business Intelligence | Power BI |
| Logging | Python `logging` module |

---

## ⚙️ Pipeline Architecture

```
Raw CSVs (6 files)
      │
      ▼
ingestion_db.py
  └─ ingest_file()       → Chunked load (100K rows) into SQLite tables
  └─ load_raw_data()     → Iterates /Data folder, logs time per file
      │
      ▼
get_vendor_summary.py
  └─ create_vendor_summary()   → 3-table SQL JOIN (purchases + sales + freight)
  └─ clean_data()              → Type casting, null fill, feature engineering
  └─ ingest_vendor_summary()   → Writes vendor_sales_summary table back to DB
      │
      ▼
Vendor_Performance_Analysis.ipynb
  └─ EDA → Filtering → 8 Business Questions → Statistical Testing
      │
      ▼
vendor_sales_summary.xlsx  →  Power BI Dashboard
```

---

## 🧪 Statistical Analysis

**Hypothesis Test: Do top and low-performing vendors differ in profit margins?**

- **H₀:** No significant difference in mean profit margins
- **H₁:** Significant difference exists
- **Result:** T-Statistic = -17.67, **P-Value ≈ 0.0000** → **Reject H₀**
- **Conclusion:** The difference is statistically significant at the 99.99% confidence level

---

## 📈 Power BI Dashboard

The dashboard covers:
- **5 KPI Cards:** Total Sales, Total Purchase, Gross Profit, Profit Margin, Unsold Capital
- **Purchase Contribution (%)** — Donut chart by vendor
- **Top Vendors by Sales** — Horizontal bar chart
- **Top Brands by Sales** — Horizontal bar chart
- **Low Performing Vendors** — Funnel chart (by Stock Turnover ratio)
- **Low Performing Brands** — Scatter plot (Sales vs Profit Margin)
- **Filters:** Vendor Name, Brand Description

---

## 🚀 How to Run

**Prerequisites:** Python 3.8+, pip

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/vendor-performance-analysis.git
cd vendor-performance-analysis

# 2. Install dependencies
pip install pandas numpy sqlalchemy scipy matplotlib seaborn openpyxl

# 3. Place raw CSV files in /Data folder

# 4. Run ingestion
python ingestion_db.py

# 5. Run vendor summary pipeline
python get_vendor_summary.py

# 6. Open notebooks in order
#    → Exploratory_Data_Analysis.ipynb
#    → Vendor_Performance_Analysis.ipynb
```



## 👤 Author

**Faisal Khan**

Data Science & AI | Finance & Economics Background

