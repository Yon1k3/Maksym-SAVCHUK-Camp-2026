SELECT
    DATE(o.created_at) AS order_date,
    COUNT(DISTINCT o.order_id) AS orders_count,
    SUM(oi.quantity) AS items_sold,
    ROUND(SUM(oi.quantity * p.price)::numeric, 2) AS revenue
FROM "shop_db"."public"."cleaned_orders" o
JOIN "shop_db"."public"."cleaned_order_items" oi
    ON o.order_id = oi.order_id
JOIN "shop_db"."public"."cleaned_products" p
    ON oi.product_id = p.product_id
WHERE o.order_status = 'completed'
GROUP BY DATE(o.created_at)
ORDER BY order_date