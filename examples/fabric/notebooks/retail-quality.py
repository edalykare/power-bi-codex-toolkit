# Fabric PySpark cell example. Local tests only compile this file; they do not run Spark.
# In Fabric, attach the intended lakehouse first. This example performs read-only checks.


def quality_summary(spark):
    """Return row and missing-key counts without printing customer records."""
    sales = spark.table("Sales")
    return {
        "rows": sales.count(),
        "missing_product_keys": sales.filter("ProductKey IS NULL").count(),
    }
