SET STATISTICS IO ON;
SET STATISTICS TIME ON;

WITH SupplierProducts AS (
    SELECT 
        s.SupplierID,
        s.CompanyName,
        p.ProductID,
        p.CategoryID
    FROM Suppliers s
    JOIN Products p WITH (INDEX(IX_Products_SupplierID_Covering))
        ON s.SupplierID = p.SupplierID
),
SupplierOrders AS (
    SELECT
        sp.SupplierID,
        sp.CategoryID,
        sp.CompanyName,
        od.Quantity,
        od.UnitPrice,
        od.Discount,
        c.CategoryName
    FROM SupplierProducts sp
    JOIN [Order Details] od ON sp.ProductID = od.ProductID
    JOIN Categories c ON sp.CategoryID = c.CategoryID
),
SupplierTotals AS (
    SELECT 
        SupplierID,
        CompanyName,
        CategoryName,
        SUM(Quantity) AS total_quantity_sold,
        ROUND(SUM(Quantity * UnitPrice * ISNULL(Discount, 0)), 2) AS total_discount,
        ROUND(SUM((UnitPrice * Quantity) * (1 - ISNULL(Discount, 0))), 2) AS total_order_revenue
    FROM SupplierOrders
    GROUP BY SupplierID, CompanyName, CategoryName
)
SELECT
    RANK() OVER (ORDER BY total_order_revenue DESC) AS revenue_rank,
    SupplierID,
    CompanyName AS SupplierName,
    RANK() OVER (PARTITION BY CategoryName ORDER BY total_order_revenue DESC) AS Category_rank,
    CategoryName,
    total_quantity_sold,
    total_discount,
    total_order_revenue
FROM SupplierTotals
ORDER BY revenue_rank;

SET STATISTICS IO OFF
SET STATISTICS TIME OFF

--CREATE INDEX IX_Products_SupplierID_Covering
--ON Products (SupplierID)
--INCLUDE (ProductID, CategoryID);