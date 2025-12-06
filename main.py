from etl.extract import load_raw_sales
from etl.transform import transform_to_star_schema, save_star_schema_tables
from warehouse.load import load_star_schema_to_db


def main():
    print("Retail ETL Project - Extract, Transform, Load")

    df_sales_raw = load_raw_sales()

    print("\nRunning transformations to build star schema...")
    dim_customer, dim_product, dim_date, fact_sales = transform_to_star_schema(df_sales_raw)

    print("\nDimCustomer:")
    print(dim_customer.head())
    print(dim_customer.info())

    print("\nDimProduct:")
    print(dim_product.head())
    print(dim_product.info())

    print("\nDimDate:")
    print(dim_date.head())
    print(dim_date.info())

    print("\nFactSales:")
    print(fact_sales.head())
    print(fact_sales.info())

    print("\nSaving tables to data/processed ...")
    save_star_schema_tables(dim_customer, dim_product, dim_date, fact_sales)

    print("\nLoading tables into PostgreSQL ...")
    load_star_schema_to_db(dim_customer, dim_product, dim_date, fact_sales)

    print("\nETL process completed.")


if __name__ == "__main__":
    main()
