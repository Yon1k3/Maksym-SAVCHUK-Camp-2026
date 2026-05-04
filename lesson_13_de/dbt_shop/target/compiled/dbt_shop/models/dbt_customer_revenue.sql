SELECT
    c.customer_id,
    c.email,
    c.country,
    COUNT(DISTINCT o.order_id) AS completed_orders,
    ROUND(SUM(oi.quantity * p.price)::numeric, 2) AS total_revenue
FROM "shop_db"."public"."cleaned_customers" c
JOIN "shop_db"."public"."cleaned_orders" o
    ON c.customer_id = o.customer_id
JOIN "shop_db"."public"."cleaned_order_items" oi
    ON o.order_id = oi.order_id
JOIN "shop_db"."public"."cleaned_products" p
    ON oi.product_id = p.product_id
WHERE o.order_status = 'completed'
GROUP BY
    c.customer_id,
    c.email,
    c.country
ORDER BY total_revenue DESC