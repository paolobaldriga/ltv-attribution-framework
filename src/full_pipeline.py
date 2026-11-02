"""
Full pipeline stub for Online Retail II.
Place data/online_retail_ii.csv and run.
Normalizes columns and produces the same CLV ranking.
"""

import pandas as pd
from lifetimes import BetaGeoFitter, GammaGammaFitter
from lifetimes.utils import summary_data_from_transaction_data
import sys

def load_and_clean(path="data/online_retail_ii.csv"):
    df = pd.read_csv(path, encoding="latin1", low_memory=False)
    # Normalize common column name variants
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    rename = {
        "invoice": "invoiceno",
        "customer_id": "customerid",
        "price": "unitprice",
    }
    df = df.rename(columns={k: v for k, v in rename.items() if k in df.columns})

    df = df.dropna(subset=["customerid"])
    df = df[df["quantity"] > 0]
    df = df[df["unitprice"] > 0]
    df["invoice_date"] = pd.to_datetime(df["invoicedate"])
    df["revenue"] = df["quantity"] * df["unitprice"]
    df["customerid"] = df["customerid"].astype(int)
    return df

def main():
    try:
        df = load_and_clean()
    except FileNotFoundError:
        print("Place Online Retail II CSV at data/online_retail_ii.csv first.")
        sys.exit(1)

    print(f"Clean rows: {len(df):,} | Customers: {df.customerid.nunique():,}")

    summary = summary_data_from_transaction_data(
        df, "customerid", "invoice_date", monetary_value_col="revenue", freq="D"
    )
    summary = summary[summary["monetary_value"] > 0]

    bgf = BetaGeoFitter(penalizer_coef=0.01)
    bgf.fit(summary["frequency"], summary["recency"], summary["T"])

    returning = summary[summary["frequency"] > 0]
    ggf = GammaGammaFitter(penalizer_coef=0.01)
    ggf.fit(returning["frequency"], returning["monetary_value"])

    summary["clv_12m"] = ggf.customer_lifetime_value(
        bgf, summary["frequency"], summary["recency"], summary["T"],
        summary["monetary_value"], time=12, freq="D", discount_rate=0.01/30
    )

    print(summary["clv_12m"].describe().round(2))
    print("\nTop 15 customers by 12m CLV:")
    print(summary.nlargest(15, "clv_12m")[["clv_12m", "frequency", "monetary_value"]].round(2))


if __name__ == "__main__":
    main()
