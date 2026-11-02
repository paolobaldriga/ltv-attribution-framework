# E-Commerce LTV & Attribution Framework

**Probabilistic Customer Lifetime Value models that turn transactional data into actionable marketing spend allocation.**

A practical framework for e-commerce and retail businesses: build cohort, attribution and LTV models that guide where the next euro of marketing spend should go, and create a trustworthy, self-serve source of truth for customer value.

> Portfolio piece by Paolo Baldriga — Marketing Measurement & AI Executive (MMM, Incrementality, CRM/Loyalty, Customer Analytics).

## Why this matters for e-commerce

Most e-commerce teams still allocate budget on last-click, ROAS or short-term revenue. High-growth and multi-category businesses need:

- Which acquisition channels and campaigns produce high-LTV customers vs. one-and-done buyers
- How early behaviour (second purchase, multi-category baskets, retention curves) predicts long-term value
- Ranking of markets, channels and segments by expected LTV and contribution margin
- A single, explainable view that Marketing, Finance and Product can trust

This framework implements that logic on real transactional data (Online Retail II as proxy) and a synthetic multi-category e-commerce generator so it runs immediately.

## What the framework delivers

| Capability | Method | Business use |
|------------|--------|--------------|
| RFM + Cohorts | Classic + retention curves | Identify loyal vs. one-shot customers |
| Probabilistic CLV | BG/NBD + Gamma-Gamma (`lifetimes`) | Individual + portfolio expected value |
| Predictive LTV | Gradient Boosting / simple regression | Early prediction from first 1–2 orders |
| Next-euro allocation | LTV by channel / market / campaign proxy | Rank where incremental spend has highest expected return |
| Margin-aware value | Adjust for assumed contribution margin | Move from revenue LTV to profit LTV |

## Quick start

```bash
pip install -r requirements.txt
python src/demo_synthetic_ltv.py          # runs in seconds on synthetic e-commerce data
# For full Online Retail II:
# 1. Download from UCI or Kaggle (see data/README.md)
# 2. Place as data/online_retail_ii.csv
# 3. python src/full_pipeline.py
```

## Key outputs (synthetic demo)

- Ranked list of customers by 12-month expected CLV
- LTV distribution and top-decile contribution
- Cohort retention and value curves
- Simple “next euro” ranking by acquisition channel
- Recommended actions (protect high-value customers, re-activate medium, suppress low-LTV acquisition)

## Architecture notes

- Modular so the same logic can sit on a real warehouse (dbt + BigQuery / Snowflake)
- Designed for self-serve: metric definitions, cohort logic and model outputs can feed Looker / Metabase / internal dashboards
- Incrementality mindset: the ranking is meant to be validated with geo or holdout tests before full budget reallocation

## Author

Paolo Baldriga  
Marketing Measurement & AI Executive  
Hamburg / Rome  
[GitHub](https://github.com/paolobaldriga)

---

*Independent portfolio project for e-commerce measurement and customer value.*
