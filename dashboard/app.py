import sys
import pathlib

import pandas as pd
import streamlit as st

project_root = pathlib.Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from config.database import get_engine


@st.cache_data
def run_query(sql: str, params: dict | None = None) -> pd.DataFrame:
    engine = get_engine()
    with engine.connect() as conn:
        df = pd.read_sql(sql, conn, params=params)
    return df


def load_sql_file(filename: str) -> str:
    sql_path = pathlib.Path(__file__).resolve().parents[1] / "sql" / filename
    with open(sql_path, "r", encoding="utf-8") as f:
        return f.read()
    

def build_filters(selected_year: int, selected_country: str, selected_segment: str):
    where_clauses = ["d.year = %(year)s"]
    params: dict = {"year": selected_year}

    if selected_country != "All":
        where_clauses.append("c.country = %(country)s")
        params["country"] = selected_country

    if selected_segment != "All":
        where_clauses.append("c.customer_segment = %(segment)s")
        params["segment"] = selected_segment

    where_clause = " AND ".join(where_clauses)
    return where_clause, params



def main():
    st.set_page_config(
        page_title="Retail Sales Analytics",
        layout="wide",
    )

    st.title("📊 Retail Sales Analytics Dashboard")
    st.write(
        "This dashboard is powered by an ETL pipeline and a PostgreSQL data warehouse "
        "(FactSales, DimCustomer, DimProduct, DimDate)."
    )


    year_bounds_sql = """
        SELECT
            MIN(year) AS min_year,
            MAX(year) AS max_year
        FROM dim_date;
    """
    year_bounds_df = run_query(year_bounds_sql)
    min_year = int(year_bounds_df["min_year"].iloc[0])
    max_year = int(year_bounds_df["max_year"].iloc[0])

    country_sql = """
        SELECT DISTINCT country
        FROM dim_customer
        ORDER BY country;
    """
    segment_sql = """
        SELECT DISTINCT customer_segment
        FROM dim_customer
        ORDER BY customer_segment;
    """

    country_df = run_query(country_sql)
    segment_df = run_query(segment_sql)

    country_options = ["All"] + country_df["country"].dropna().tolist()
    segment_options = ["All"] + segment_df["customer_segment"].dropna().tolist()

    st.sidebar.header("Controls")

    if min_year >= max_year:
        years = [min_year]
        selected_year = st.sidebar.selectbox("Select Year", years, index=0)
    else:
        selected_year = st.sidebar.slider(
            "Select Year",
            min_value=min_year,
            max_value=max_year,
            value=max_year,
            step=1,
        )

    selected_country = st.sidebar.selectbox(
        "Country",
        options=country_options,
        index=0, 
    )

    selected_segment = st.sidebar.selectbox(
        "Customer segment",
        options=segment_options,
        index=0, 
    )

    st.sidebar.write(f"Year: {selected_year}")
    st.sidebar.write(f"Country: {selected_country}")
    st.sidebar.write(f"Segment: {selected_segment}")


    st.subheader("Key Performance Indicators")

    where_clause, kpi_params = build_filters(selected_year, selected_country, selected_segment)

    kpi_sql = f"""
        SELECT
            COUNT(DISTINCT f.order_id) AS total_orders,
            COUNT(DISTINCT f.customer_id) AS total_customers,
            SUM(f.net_revenue) AS total_revenue
        FROM fact_sales f
        JOIN dim_date d
            ON f.date_key = d.date_key
        JOIN dim_customer c
            ON f.customer_id = c.customer_id
        WHERE {where_clause};
    """
    kpi_df = run_query(kpi_sql, params=kpi_params)


    total_orders = int(kpi_df["total_orders"].iloc[0])
    total_customers = int(kpi_df["total_customers"].iloc[0])
    total_revenue = float(kpi_df["total_revenue"].iloc[0])

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Orders", f"{total_orders}")
    col2.metric("Total Customers", f"{total_customers}")
    col3.metric("Total Revenue", f"${total_revenue:,.2f}")

    st.subheader("Monthly Revenue Trend")

    monthly_sql = """
        SELECT
            d.year,
            d.month,
            d.month_name,
            SUM(f.net_revenue) AS total_revenue
        FROM fact_sales f
        JOIN dim_date d
            ON f.date_key = d.date_key
        WHERE d.year = %(year)s
        GROUP BY
            d.year,
            d.month,
            d.month_name
        ORDER BY
            d.year,
            d.month;
    """
    monthly_df = run_query(monthly_sql, params={"year": selected_year})


    monthly_df["year_month"] = (
        monthly_df["year"].astype(str)
        + "-"
        + monthly_df["month"].astype(str).str.zfill(2)
    )

    st.line_chart(
        data=monthly_df,
        x="year_month",
        y="total_revenue",
    )

    st.subheader("Top Products by Revenue")

    where_clause, product_params = build_filters(selected_year, selected_country, selected_segment)

    top_products_sql = f"""
        SELECT
            p.product_id,
            p.product_name,
            SUM(f.quantity) AS total_quantity_sold,
            SUM(f.net_revenue) AS total_revenue
        FROM fact_sales f
        JOIN dim_product p
            ON f.product_id = p.product_id
        JOIN dim_date d
            ON f.date_key = d.date_key
        JOIN dim_customer c
            ON f.customer_id = c.customer_id
        WHERE {where_clause}
        GROUP BY
            p.product_id,
            p.product_name
        ORDER BY
            total_revenue DESC
        LIMIT 10;
    """
    top_products_df = run_query(top_products_sql, params=product_params)



    st.bar_chart(
        data=top_products_df.set_index("product_name")["total_revenue"]
    )

    st.dataframe(top_products_df)

    st.subheader("Revenue by Customer Segment")

    where_clause, segment_params = build_filters(selected_year, selected_country, selected_segment)

    segment_sql = f"""
        SELECT
            c.customer_segment,
            SUM(f.net_revenue) AS total_revenue,
            COUNT(DISTINCT f.customer_id) AS unique_customers
        FROM fact_sales f
        JOIN dim_customer c
            ON f.customer_id = c.customer_id
        JOIN dim_date d
            ON f.date_key = d.date_key
        WHERE {where_clause}
        GROUP BY
            c.customer_segment
        ORDER BY
            total_revenue DESC;
    """
    segment_df = run_query(segment_sql, params=segment_params)


    st.bar_chart(
        data=segment_df.set_index("customer_segment")["total_revenue"]
    )

    st.dataframe(segment_df)


if __name__ == "__main__":
    main()
