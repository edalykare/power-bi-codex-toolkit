-- Review schema names against the selected Warehouse before executing.
SELECT
    COUNT_BIG(*) AS RowCount,
    SUM(CASE WHEN ProductKey IS NULL THEN 1 ELSE 0 END) AS MissingProductKeys
FROM dbo.Sales;
