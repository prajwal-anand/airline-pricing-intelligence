# ✈️ Airline Pricing Intelligence & Market Analytics Framework

## 📌 Project Overview

This project analyzes airline ticket pricing behavior and builds a predictive pricing validation model using structured analytics, feature engineering, and machine learning.

It demonstrates:

- Structured exploratory data analysis (EDA)
- Advanced feature engineering
- Pricing behavior insights
- Modular Python architecture
- Predictive modeling with validation
- Executive-level storytelling

---

## 📊 Key Business Questions

1. How do stops and duration impact ticket price?
2. Do airlines price above or below route averages?
3. Are premium airlines consistently priced higher?
4. Can structured features predict airline ticket prices?

---

## 📂 Project Structure
```
airline-pricing-intelligence/
│
├── data/
│ └── flight_price.xlsx
│
├── docs/
│ └── executive_summary.md
│
├── outputs/
│ ├── correlation_map.png
│ └── feature_importance.png
│
├── src/
│ ├── data_loader.py
│ ├── preprocessing.py
│ ├── analysis.py
│ ├── model.py
│ └── run_pipeline.py
│
├── requirements.txt
└── README.md
```
---

## 🔍 Analytical Insights

### 1️⃣ Stops vs Price
Flights with more stops are significantly more expensive.  
Mean price increases from ₹5,024 (non-stop) to ₹17,686 (4 stops).

### 2️⃣ Correlation Analysis
- Total Stops → 0.60 correlation with Price
- Duration → 0.51 correlation with Price

Stops influence pricing more than duration.

### 3️⃣ Brand Pricing Strategy
Premium airlines (Jet Airways Business, Vistara Premium) consistently price above route averages.

Low-cost carriers (GoAir, SpiceJet) price below.

This indicates brand-driven pricing power.

---

## 🤖 Predictive Model

Model: Random Forest Regressor

Performance:

- **R² Score:** 0.79  
- **MAE:** ₹1,279  

The model explains 79% of price variance using structured features.

Top Predictive Features:

- Total Duration (minutes)
- Day of Journey
- Airline (Brand effect)
- Month of Journey
- Total Stops

---

## 🛠 Tech Stack

- Python
- pandas
- numpy
- seaborn
- matplotlib
- scikit-learn

---

## 🚀 How to Run

```bash
python -m src.run_pipeline

---

## 👤 Author

**Prajwal Anand**
Data Analytics | Pricing Intelligence | Machine Learning

---