"""
Synthetic multi-category e-commerce LTV demo.
Generates orders that mimic multi-item baskets, market mix and acquisition channels,
then runs RFM + BG/NBD + Gamma-Gamma and produces a simple next-euro ranking.
"""

import pandas as pd
import numpy as np
from lifetimes import BetaGeoFitter, GammaGammaFitter
from lifetimes.utils import summary_data_from_transaction_data
from datetime import datetime, timedelta

np.random.seed(42)

def generate_synthetic_ecommerce_data(n_customers=2500, days=540):
    markets = ["DE", "FR", "IT", "ES", "NL", "BE", "AT", "Other"]
    channels = ["Meta", "Google", "Organic", "Email", "Influencer", "Direct"]
    categories = ["Electronics", "Fashion", "Home", "Beauty", "Sports", "Books"]

    rows = []
    start = datetime(2024, 6, 1)

    for cid in range(1, n_customers + 1):
        market = np.random.choice(markets, p=[0.28, 0.18, 0.12, 0.10, 0.08, 0.07, 0.05, 0.12])
        channel = np.random.choice(channels, p=[0.30, 0.22, 0.18, 0.12, 0.10, 0.08])
        # Loyal / high-value propensity
        loyal = np.random.random() < 0.40
        n_orders = np.random.poisson(1.8 if loyal else 0.9) + 1
        n_orders = min(n_orders, 12)

        first_order = start + timedelta(days=int(np.random.exponential(120)))
        if first_order > start + timedelta(days=days):
            continue

        for o in range(n_orders):
            order_date = first_order + timedelta(days=int(np.random.exponential(45) * (o + 1)))
            if order_date > start + timedelta(days=days):
                break
            n_items = np.random.choice([1, 2, 3, 4, 5], p=[0.20, 0.35, 0.25, 0.12, 0.08] if loyal else [0.50, 0.30, 0.12, 0.05, 0.03])
            for _ in range(n_items):
                category = np.random.choice(categories)
                base_price = np.random.uniform(15, 120)
                price = round(base_price * np.random.uniform(0.85, 1.25), 2)
                rows.append({
                    "customer_id": cid,
                    "order_date": order_date,
                    "product": f"{category}_{np.random.randint(1000,9999)}",
                    "category": category,
                    "price": price,
                    "market": market,
                    "channel": channel,
                    "is_loyal": loyal
                })

    df = pd.DataFrame(rows)
    return df

def main():
    print("Generating synthetic multi-category e-commerce orders...")
    df = generate_synthetic_ecommerce_data()
    print(f"Orders generated: {len(df):,} | Customers: {df.customer_id.nunique():,}")

    # Transaction summary for lifetimes
    summary = summary_data_from_transaction_data(
        df, "customer_id", "order_date", monetary_value_col="price", freq="D"
    )
    summary = summary[summary["monetary_value"] > 0].copy()

    print(f"\nCustomers in summary: {len(summary):,}")
    print(summary.describe().round(2))

    # BG/NBD
    bgf = BetaGeoFitter(penalizer_coef=0.01)
    bgf.fit(summary["frequency"], summary["recency"], summary["T"])
    print("\nBG/NBD fitted:")
    print(bgf.summary)

    # Gamma-Gamma on repeaters
    returning = summary[summary["frequency"] > 0]
    ggf = GammaGammaFitter(penalizer_coef=0.01)
    ggf.fit(returning["frequency"], returning["monetary_value"])
    print("\nGamma-Gamma fitted:")
    print(ggf.summary)

    # 12-month CLV
    summary["clv_12m"] = ggf.customer_lifetime_value(
        bgf,
        summary["frequency"],
        summary["recency"],
        summary["T"],
        summary["monetary_value"],
        time=12,
        freq="D",
        discount_rate=0.01 / 30,  # approx monthly
    )

    # Attach first channel / market
    first = df.sort_values("order_date").groupby("customer_id").first()[["channel", "market"]]
    summary = summary.join(first)

    # Next-euro ranking by channel (mean CLV, simple proxy)
    channel_ltv = (
        summary.groupby("channel")["clv_12m"]
        .agg(["count", "mean", "median", "sum"])
        .sort_values("mean", ascending=False)
        .round(2)
    )
    print("\n=== Next-euro proxy: mean 12m CLV by acquisition channel ===")
    print(channel_ltv)

    print("\n=== Top 10 customers by predicted 12m CLV ===")
    print(summary.nlargest(10, "clv_12m")[["clv_12m", "frequency", "monetary_value", "channel", "market"]].round(2))

    print("\nPortfolio 12m expected CLV (sum):", round(summary["clv_12m"].sum(), 0))
    print("Top 10% of customers contribute:", 
          round(100 * summary.nlargest(int(0.1 * len(summary)), "clv_12m")["clv_12m"].sum() / summary["clv_12m"].sum(), 1), "%")

    print("\n--- Recommended actions for e-commerce ---")
    print("1. Protect and upsell high-CLV customers (multi-category, repeat buyers).")
    print("2. Use early behavioural signals (2nd purchase within 30 days) as a strong LTV predictor.")
    print("3. Re-allocate test budget toward channels with higher mean CLV after geo/holdout validation.")
    print("4. Build self-serve cohort + LTV dashboards so Marketing and Finance see the same numbers.")


if __name__ == "__main__":
    main()
