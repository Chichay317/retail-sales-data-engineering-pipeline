SELECT
    c.customer_segment,
    SUM(f.net_revenue) AS total_revenue,
    COUNT(DISTINCT f.customer_id) AS unique_customers
FROM fact_sales f
JOIN dim_customer c
    ON f.customer_id = c.customer_id
GROUP BY
    c.customer_segment
ORDER BY
    total_revenue DESC;
