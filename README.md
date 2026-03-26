# 🏨 Hotel Revenue Management Dashboard

![Python](https://img.shields.io/badge/Python-3.11-blue)
![SQL](https://img.shields.io/badge/SQL-MySQL-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![Status](https://img.shields.io/badge/Status-Complete-success)

## 🚀 Live Dashboard
**[Click here to open the dashboard](https://hotel-revenue-dashboard-bi.streamlit.app/)**

## 🎯 Project Overview

Interactive dashboard analyzing **36,000+ real hotel reservations** to identify revenue optimization opportunities, cancellation patterns, and strategic pricing insights.

**Dataset:** Hotel Reservations Classification Dataset (Kaggle)  
**Period:** 18 months of data  
**Total Revenue Analyzed:** $7,028,557.32

---

## DataTools & Technologies

- **SQL (MySQL):** Complex queries, CASE WHEN, aggregations, date functions
- **Python 3.11:** Data cleaning, analysis, and visualization
- **Pandas:** Data manipulation and feature engineering
- **Plotly:** Interactive visualizations
- **Streamlit:** Interactive web dashboard
- **SQLAlchemy:** Database connectivity

---

## 📁 Project Structure
```
hotel-revenue-dashboard/
│
├── .streamlit/
│   └── config.toml                     # Dark theme configuration
├── data/                                # Raw data
│   └── hotel_reservations.csv          # Original dataset (Kaggle)
├── sql/
│   └── hotel_analysis.sql              # All SQL queries
├── notebooks/
│   └── exploration.ipynb               # Data exploration & cleaning
├── app/
│   ├── dashboard.py                    # Dashboard (MySQL version)
│   ├── dashboard_deploy.py             # Dashboard (deployed version)
│   └── hotel_reservations_clean.csv    # Cleaned dataset
├── requirements.txt                    # Python dependencies
├── .gitignore
├── README.md                           # This file
└── project_notes.txt                   # Technical documentation
```

---

## 🔍 Key Analyses

### 1️⃣ Revenue by Market Segment
**Business Question:** "Where should we invest our marketing budget?"

**Key Findings:**
- **Online** leads in total revenue ($4,869,836) and ADR ($112.74)
- However, Online also has the **highest cancellation volume** (8,429)
- **Corporate** segment is most reliable (only 220 cancellations) despite lower ADR ($82.91)

**Recommendation:** Implement stricter cancellation policies for Online bookings while offering loyalty incentives to Corporate clients.

---

### 2️⃣ Monthly Revenue Trend
**Business Question:** "When should we increase prices? When to promote?"

**Key Findings:**
- Peak revenue in months **August-October**
- Seasonality pattern suggests non-European destination
- Consistent growth trend across analyzed period

**Recommendation:** Implement dynamic pricing strategy with +15-20% premium during peak months (Aug-Oct).

---

### 3️⃣ Cancellation Analysis by Lead Time
**Business Question:** "What factors influence cancellations?"

**Key Findings:**

| Booking Window | Cancellation Rate | Strategy |
|----------------|-------------------|----------|
| Very Early (180+ days) | 73.8% ❌ | Non-refundable rate with 20-25% discount |
| Early (90-179 days) | ~45% ⚠️ | Semi-flexible policy |
| Standard (30-89 days) | 25% ⚠️ | Free cancel up to 15 days before |
| Short Notice (7-29 days) | 18% ✅ | Semi-flexible policy |
| Last Minute (0-6 days) | ~10% ✅ | Dynamic pricing premium (+20-30%) |

**Key Insight:** The longer in advance a booking is made, the higher the chance of cancellation. Very Early bookings have a 73.8% cancellation rate despite having the highest volume (5,366 reservations).

---

### 4️⃣ Room Type Performance
**Business Question:** "Which rooms should we invest in? Which to phase out?"

**Key Findings:**

| Room Type | Status | Action |
|-----------|--------|--------|
| **Type 1** | Cash cow - highest volume (28,063) but low ADR ($93.48) | Test gradual ADR increase (+$5-7) |
| **Type 2** | Underperformer - low volume, low ADR, high cancellation | Phase out or convert |
| **Type 5** | Hidden gem - lowest cancellation (27.2%), good ADR ($118.31) | Increase marketing visibility |
| **Type 6** | Premium opportunity - highest ADR ($178.53) but 42.2% cancellation | Non-refundable rate with perks |

---

## 💡 Business Recommendations

### 🎯 Revenue Optimization
1. **Test ADR increase on Room Type 1** (+$7 = potential +$196k/year)
2. **Dynamic pricing for last-minute bookings** (+20-30% premium)
3. **Peak season pricing** (+15-20% during Aug-Oct)

### 🔄 Cancellation Reduction
1. **Non-refundable advance purchase rate** for bookings 180+ days out (with 20-25% discount)
2. **Semi-flexible policy** for Standard bookings (free cancel up to 15 days before)
3. **Deposit requirement** for Very Early bookings

### 🏆 Portfolio Optimization
1. **Invest in Room Type 5** (hidden gem with best reliability)
2. **Develop Room Type 6** (premium segment with perks strategy)
3. **Phase out Room Type 2** (underperformer)

---

## 📊 Dashboard Features

- 🔍 **Interactive Filters:** Year, Market Segment, Room Type, Booking Status
- 📈 **4 Dynamic Charts:** Revenue by Segment, Monthly Trend, Cancellation Analysis, Room Performance
- 💰 **Real-time KPIs:** Total Revenue, ADR, Confirmation Rate
- 📋 **Detailed Data Tables:** Expandable data views

---

## 🚀 How to Run Locally

### 1. Clone repository
```bash
git clone https://github.com/Luiz-mila/hotel-revenue-dashboard.git
cd hotel-revenue-dashboard
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run dashboard
```bash
cd app
streamlit run dashboard_deploy.py
```

### 4. Access dashboard
Open browser: `http://localhost:8501`

---

## 📈 Skills Demonstrated

**SQL:**
- Complex CASE WHEN aggregations
- GROUP BY with multiple dimensions
- Conditional aggregations (SUM/AVG with CASE WHEN)
- Date functions and time series analysis

**Python:**
- Data cleaning and feature engineering
- Statistical analysis and KPI calculation
- Interactive visualizations with Plotly
- Streamlit dashboard development

**Business Intelligence:**
- Revenue management strategy
- Cancellation pattern analysis
- Dynamic pricing recommendations
- Portfolio optimization insights

---

## 🎓 About Me

**Data Analyst | SQL & Python | Streamlit Developer**

- 🇫🇷 Based in France
- 🌍 Languages: Portuguese, French, English, Italian
- 💼 Open to opportunities in Europe
- 🏨 3+ years hospitality industry experience
- 🎯 Passionate about transforming data into actionable business insights

---

## 📧 Contact

LinkedIn: https://www.linkedin.com/in/luiz-milar%C3%A9-a5869519a/

Email: luizmilare958@gmail.com

GitHub: github.com/Luiz-mila

Location: Paris, France 🇫🇷

---

## 📝 Data Source

**Dataset:** [Hotel Reservations Classification Dataset](https://www.kaggle.com/datasets/ahsan81/hotel-reservations-classification-dataset)  
**License:** MIT

---

*Built as part of a data analytics portfolio to demonstrate proficiency in SQL, Python, and business intelligence.*
