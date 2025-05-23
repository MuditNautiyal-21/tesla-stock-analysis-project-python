# 📈 Tesla Stock Price Analysis using Regression, Clustering, and SQL

## 🚀 Overview
This project analyzes historical Tesla (TSLA) stock data using statistical modeling, clustering, and relational database techniques. It aims to understand stock behavior, engineer features, and build interpretable models — all backed by SQL-integrated pipelines.

---

## 📊 Dataset
- 📅 **Timeframe**: Multiple years of daily Tesla stock prices
- 📦 **Source**: `TSLA.csv` (includes Open, High, Low, Close, Adj Close, Volume)
- 🔁 **Resampling**: Monthly average data calculated for time-based trends

---

## 🎯 Objectives
- Clean and structure Tesla stock data
- Engineer features (e.g., moving averages)
- Store, query, and normalize data using SQLite
- Predict closing price using regression models
- Cluster historical stock behavior using KMeans

---

## 🧠 Key Techniques Used
- 📐 **Data Cleaning**: Duplicate removal, outlier detection (IQR), missing value handling (FFill)
- 🧮 **Feature Engineering**: 
  - `Close_MA_3` → 3-month moving average  
  - Time grouping for monthly analysis
- 📊 **Modeling**:
  - `Linear Regression` using Open, High, Low, Volume
  - `KMeans Clustering` on numerical features
- 🧩 **SQL Integration**:
  - Used SQLite to store, query, and validate stock data
  - Verified 1NF, 2NF, 3NF compliance
  - Executed SQL transactions and created data views

---

## 🧪 Regression Model Results

| Metric         | Value     |
|----------------|-----------|
| **Model**      | Linear Regression |
| **RMSE**       | 4.25      |
| **Predictors** | Open, High, Low, Volume |
| **Target**     | Close     |

> Interpreted OLS regression summary to assess p-values and significance of predictors.

---

## 📊 K-Means Clustering

- Clustered stock records into 3 behavioral segments
- Visualized clusters using Open vs Close price scatter plots
- Useful for pattern discovery and potential risk segmentation

---

## 🗃️ SQL & Database Highlights

- ✅ Created SQLite database `Tesla_Database.db`
- 🗂️ Table: `TSLA_Prices` (custom schema)
- 📋 Queries:
  - High-volume day filter
  - Monthly averages
  - Transactional inserts
  - Views for analytical queries
- 📐 Verified:
  - Atomicity (1NF)
  - Functional dependency (2NF)
  - Transitive dependency (3NF)

---

## 📈 Visual Highlights

- 📦 Boxplots: Outliers before and after removal
- 📊 Histograms: Distribution of Close prices (pre/post normalization)
- 🧭 Line and bar plots: Monthly average close price
- 🔍 Heatmap: Correlation matrix of all key variables

---

## 📂 Folder Structure
📦 Tesla-Stock-Analysis
├── TSLA.csv
├── Mudit_Nautiyal_EAS503_Final_Project.ipynb
├── Tesla_Database.db
├── README.md
└── requirements.txt
