Retail Sales Data Engineering Pipeline

Python • Pandas • PostgreSQL • SQLAlchemy • Streamlit • Dimensional Modelling

This project demonstrates a complete end-to-end data engineering workflow, from raw data ingestion to analytics dashboard, using a dimensional data warehouse.

Project Architecture

ETL Pipeline

Extract: Raw retail sales data generated and ingested using Python and Pandas.

Transform:
(a) Cleaned and enriched dataset.

(b) Dimensional modelling with star schema: FactSales, DimCustomer, DimProduct, DimDate

Load: Tables loaded into PostgreSQL warehouse via SQLAlchemy.

Analytics & Dashboard: Streamlit dashboard with:
(a) KPIs

(b) Monthly revenue trends

(c) Top products

(d) Revenue by customer segment

(e) Filters (Year, Country, Customer Segment)


What This Project Demonstrates
(a) ETL engineering

(b) Data modelling (star schema)

(c) SQL analytics

(d) Building a PostgreSQL warehouse

(e) Python automation with Pandas + SQLAlchemy

(f) Interactive BI dashboard development

(g) Parameterised SQL + dynamic filtering


Future Improvements:
(a) Airflow orchestration

(b) Docker containerisation

(c) Cloud deployment (Streamlit Cloud + Neon/Postgres)
