# Setup and run

Project structure after adding optional tasks:

```text
lesson_13_de/
│
├── docker-compose.yml
├── profiles.yml
├── lesson_13_de_hometask.ipynb
├── shop_analytics_sqlite.db
│
├── dbt_shop/
│   ├── dbt_project.yml
│   └── models/
│       ├── sources.yml
│       ├── dbt_daily_sales.sql
│       ├── dbt_customer_revenue.sql
│       ├── dbt_product_sales.sql
│       └── dbt_category_sales.sql
│
├── tests/
│   └── test_data_quality.py
│
└── data/
    ├── customers.csv
    ├── orders.csv
    ├── order_items.csv
    └── products.csv
```

Install Python packages:

```bash
pip install pandas sqlalchemy psycopg2-binary matplotlib pytest pyspark dbt-core dbt-postgres
```

Start PostgreSQL:

```bash
docker compose up -d
```

Check container:

```bash
docker ps
```

Run the main notebook cells from top to bottom.

Optional

Run pytest tests:

```bash
pytest tests/test_data_quality.py -q
```

Run dbt models:

```bash
cd dbt_shop
dbt debug --profiles-dir ..
dbt run --profiles-dir ..
```

Optional parts added to the project:

- `pytest` was added for automatic data quality checks;
- `SQLite` was added as an additional local database;
- `PySpark` was added as an additional processing example;
- `dbt` was added for SQL-based analytical transformations.
