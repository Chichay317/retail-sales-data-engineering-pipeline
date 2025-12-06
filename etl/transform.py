from pathlib import Path
from typing import Tuple

import pandas as pd


def add_derived_columns(df_raw: pd.DataFrame) -> pd.DataFrame:
    df = df_raw.copy()

    df["gross_amount"] = df["unit_price"] * df["quantity"]
    df["discount_amount"] = df["gross_amount"] * df["discount"]
    df["net_revenue"] = df["gross_amount"] - df["discount_amount"]

    if not pd.api.types.is_datetime64_any_dtype(df["order_date"]):
        df["order_date"] = pd.to_datetime(df["order_date"])

    df["date_key"] = df["order_date"].dt.strftime("%Y%m%d").astype(int)

    return df


def build_dim_customer(df: pd.DataFrame) -> pd.DataFrame:
    dim_customer = (
        df[
            [
                "customer_id",
                "customer_name",
                "customer_email",
                "customer_segment",
                "city",
                "country",
            ]
        ]
        .drop_duplicates()
        .sort_values("customer_id")
        .reset_index(drop=True)
    )

    return dim_customer


def build_dim_product(df: pd.DataFrame) -> pd.DataFrame:
    dim_product = (
        df[
            [
                "product_id",
                "product_name",
                "product_category",
                "product_subcategory",
                "unit_price",
            ]
        ]
        .drop_duplicates()
        .sort_values("product_id")
        .reset_index(drop=True)
    )

    return dim_product


def build_dim_date(df: pd.DataFrame) -> pd.DataFrame:
    dates = df[["order_date", "date_key"]].drop_duplicates().copy()
    dates = dates.sort_values("order_date").reset_index(drop=True)

    dim_date = pd.DataFrame()
    dim_date["date_key"] = dates["date_key"]
    dim_date["date"] = dates["order_date"]
    dim_date["year"] = dim_date["date"].dt.year
    dim_date["month"] = dim_date["date"].dt.month
    dim_date["day"] = dim_date["date"].dt.day
    dim_date["month_name"] = dim_date["date"].dt.strftime("%B")
    dim_date["quarter"] = dim_date["date"].dt.quarter

    return dim_date


def build_fact_sales(df: pd.DataFrame) -> pd.DataFrame:
    fact_sales = df[
        [
            "order_id",
            "date_key",
            "customer_id",
            "product_id",
            "quantity",
            "unit_price",
            "discount",
            "gross_amount",
            "discount_amount",
            "net_revenue",
            "payment_method",
        ]
    ].copy()

    return fact_sales


def transform_to_star_schema(
    df_raw: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    df_enriched = add_derived_columns(df_raw)

    dim_customer = build_dim_customer(df_enriched)
    dim_product = build_dim_product(df_enriched)
    dim_date = build_dim_date(df_enriched)
    fact_sales = build_fact_sales(df_enriched)

    return dim_customer, dim_product, dim_date, fact_sales


def save_star_schema_tables(
    dim_customer: pd.DataFrame,
    dim_product: pd.DataFrame,
    dim_date: pd.DataFrame,
    fact_sales: pd.DataFrame,
    output_dir: str = "data/processed",
) -> None:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    dim_customer_path = output_path / "dim_customer.csv"
    dim_product_path = output_path / "dim_product.csv"
    dim_date_path = output_path / "dim_date.csv"
    fact_sales_path = output_path / "fact_sales.csv"

    dim_customer.to_csv(dim_customer_path, index=False)
    dim_product.to_csv(dim_product_path, index=False)
    dim_date.to_csv(dim_date_path, index=False)
    fact_sales.to_csv(fact_sales_path, index=False)

    print(f"Saved DimCustomer to: {dim_customer_path}")
    print(f"Saved DimProduct to: {dim_product_path}")
    print(f"Saved DimDate to: {dim_date_path}")
    print(f"Saved FactSales to: {fact_sales_path}")
