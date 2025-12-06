import pandas as pd
from sqlalchemy.engine import Engine

from config.database import get_engine


def load_dataframe_to_db(df: pd.DataFrame, table_name: str, engine: Engine) -> None:
    print(f"Loading table '{table_name}' into database...")
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"Finished loading table '{table_name}'.\n")


def load_star_schema_to_db(
    dim_customer: pd.DataFrame,
    dim_product: pd.DataFrame,
    dim_date: pd.DataFrame,
    fact_sales: pd.DataFrame,
) -> None:
    engine = get_engine()

    load_dataframe_to_db(dim_customer, "dim_customer", engine)
    load_dataframe_to_db(dim_product, "dim_product", engine)
    load_dataframe_to_db(dim_date, "dim_date", engine)
    load_dataframe_to_db(fact_sales, "fact_sales", engine)

    print("All star schema tables loaded into PostgreSQL.")
