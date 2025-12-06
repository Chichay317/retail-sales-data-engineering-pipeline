SELECT
    d.year,
    d.month,
    d.month_name,
    SUM(f.net_revenue) AS total_revenue
FROM fact_sales f
JOIN dim_date d
    ON f.date_key = d.date_key
GROUP BY
    d.year,
    d.month,
    d.month_name
ORDER BY
    d.year,
    d.month;
