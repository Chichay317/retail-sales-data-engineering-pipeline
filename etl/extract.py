from pathlib import Path
from typing import Optional

import pandas as pd


def load_raw_sales(csv_path: Optional[str] = None) -> pd.DataFrame:
    if csv_path is None:
        csv_path = "data/raw/sales_raw.csv"

    path = Path(csv_path)

    if not path.exists():
        raise FileNotFoundError(f"Raw sales file not found at: {path}")

    df = pd.read_csv(path, parse_dates=["order_date"])

    print(f"Loaded raw sales data from: {path}")
    print(f"Number of rows: {len(df)}")
    print("Columns:", list(df.columns))
    print()
    print("Sample rows:")
    print(df.head())

    return df
