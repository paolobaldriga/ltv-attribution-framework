# Data

## Synthetic demo (recommended for first run)

`python src/demo_synthetic_ltv.py` generates a small multi-category e-commerce dataset in memory. No download required.

## Full Online Retail II (proxy for multi-product e-commerce)

1. Download the UCI Online Retail II dataset:  
   https://archive.ics.uci.edu/dataset/502/online+retail+ii  
   or any cleaned Kaggle mirror (search “Online Retail II”).

2. Convert the Excel to CSV if needed and place it as:  
   `data/online_retail_ii.csv`

3. Expected columns (names are normalized in the pipeline):
   - InvoiceNo / Invoice
   - StockCode
   - Description
   - Quantity
   - InvoiceDate
   - UnitPrice / Price
   - CustomerID
   - Country

License of the original dataset: CC BY 4.0 (UCI).

The methodology (RFM → BG/NBD + Gamma-Gamma → next-euro ranking) transfers directly to any e-commerce transaction log with customer ID, order date, revenue and acquisition source.
