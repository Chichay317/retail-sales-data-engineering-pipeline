SELECT
    p.product_id,
    p.product_name,
    SUM(f.quantity) AS total_quantity_sold,
    SUM(f.net_revenue) AS total_revenue
FROM fact_sales f
JOIN dim_product p
    ON f.product_id = p.product_id
GROUP BY
    p.product_id,
    p.product_name
ORDER BY
    total_revenue DESC
LIMIT 10;
