SELECT
    p.category,
    COUNT(DISTINCT o.order_id) AS orders_count,
    SUM(oi.quantity) AS units_sold,
    ROUND(SUM(oi.quantity * p.price)::numeric, 2) AS total_revenue
FROM {{ source('shop', 'cleaned_products') }} p
JOIN {{ source('shop', 'cleaned_order_items') }} oi
    ON p.product_id = oi.product_id
JOIN {{ source('shop', 'cleaned_orders') }} o
    ON oi.order_id = o.order_id
WHERE o.order_status = 'completed'
GROUP BY p.category
ORDER BY total_revenue DESC