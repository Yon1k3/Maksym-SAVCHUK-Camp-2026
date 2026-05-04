import pandas as pd
from sqlalchemy import create_engine, text


DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/shop_db"
engine = create_engine(DATABASE_URL)


def read_table(table_name):
    return pd.read_sql_query(f"SELECT * FROM {table_name};", engine)


def test_cleaned_tables_exist():
    expected_tables = {
        "cleaned_customers",
        "cleaned_products",
        "cleaned_orders",
        "cleaned_order_items",
        "mart_daily_sales",
        "mart_customer_revenue",
        "mart_product_sales",
        "mart_category_sales",
        "mart_data_quality",
    }

    query = """
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public';
    """

    existing_tables = set(pd.read_sql_query(query, engine)["table_name"])

    assert expected_tables.issubset(existing_tables)


def test_customer_ids_are_unique():
    customers = read_table("cleaned_customers")

    assert customers["customer_id"].isna().sum() == 0
    assert customers["customer_id"].duplicated().sum() == 0


def test_product_ids_are_unique():
    products = read_table("cleaned_products")

    assert products["product_id"].isna().sum() == 0
    assert products["product_id"].duplicated().sum() == 0


def test_order_ids_are_unique():
    orders = read_table("cleaned_orders")

    assert orders["order_id"].isna().sum() == 0
    assert orders["order_id"].duplicated().sum() == 0


def test_product_prices_are_positive():
    products = read_table("cleaned_products")

    assert (products["price"] > 0).all()


def test_order_item_quantities_are_positive():
    order_items = read_table("cleaned_order_items")

    assert (order_items["quantity"] > 0).all()


def test_order_statuses_are_valid():
    orders = read_table("cleaned_orders")
    valid_statuses = {"completed", "pending", "cancelled"}

    assert set(orders["order_status"]).issubset(valid_statuses)


def test_orders_have_existing_customers():
    query = """
    SELECT COUNT(*) AS broken_refs
    FROM cleaned_orders o
    LEFT JOIN cleaned_customers c
        ON o.customer_id = c.customer_id
    WHERE c.customer_id IS NULL;
    """

    result = pd.read_sql_query(query, engine)

    assert result.loc[0, "broken_refs"] == 0


def test_order_items_have_existing_orders():
    query = """
    SELECT COUNT(*) AS broken_refs
    FROM cleaned_order_items oi
    LEFT JOIN cleaned_orders o
        ON oi.order_id = o.order_id
    WHERE o.order_id IS NULL;
    """

    result = pd.read_sql_query(query, engine)

    assert result.loc[0, "broken_refs"] == 0


def test_order_items_have_existing_products():
    query = """
    SELECT COUNT(*) AS broken_refs
    FROM cleaned_order_items oi
    LEFT JOIN cleaned_products p
        ON oi.product_id = p.product_id
    WHERE p.product_id IS NULL;
    """

    result = pd.read_sql_query(query, engine)

    assert result.loc[0, "broken_refs"] == 0