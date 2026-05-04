
  
    

  create  table "shop_db"."public"."dbt_product_sales__dbt_tmp"
  
  
    as
  
  (
    SELECT
    p.product_id,
    p.name,
    p.category,
    SUM(oi.quantity) AS units_sold,
    ROUND(SUM(oi.quantity * p.price)::numeric, 2) AS total_revenue
FROM "shop_db"."public"."cleaned_products" p
JOIN "shop_db"."public"."cleaned_order_items" oi
    ON p.product_id = oi.product_id
JOIN "shop_db"."public"."cleaned_orders" o
    ON oi.order_id = o.order_id
WHERE o.order_status = 'completed'
GROUP BY
    p.product_id,
    p.name,
    p.category
ORDER BY total_revenue DESC
  );
  