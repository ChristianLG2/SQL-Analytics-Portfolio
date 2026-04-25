-- USE Northwind;
-- GO

-- Business question: How has monthly revenue trended?
-- What is the month-over-month growth rate and 3-month rolling average?


WITH MonthlySales AS (
    SELECT
        DATEFROMPARTS(YEAR(o.OrderDate), MONTH(o.OrderDate), 1) AS SaleMonth,
        SUM(od.UnitPrice * od.Quantity * (1 - od.Discount))     AS MonthlyRevenue
    FROM Orders o
    JOIN [Order Details] od ON o.OrderID = od.OrderID
    WHERE o.OrderDate IS NOT NULL
    GROUP BY DATEFROMPARTS(YEAR(o.OrderDate), MONTH(o.OrderDate), 1)
)
SELECT
    SaleMonth,
    ROUND(MonthlyRevenue, 2)                                          AS MonthlyRevenue,
    ROUND(LAG(MonthlyRevenue, 1) OVER (ORDER BY SaleMonth), 2)       AS PriorMonthRevenue,
    ROUND(
        (MonthlyRevenue - LAG(MonthlyRevenue, 1) OVER (ORDER BY SaleMonth))
        / NULLIF(LAG(MonthlyRevenue, 1) OVER (ORDER BY SaleMonth), 0) * 100
    , 1)                                                              AS MoMGrowthPct,
    ROUND(
        AVG(MonthlyRevenue) OVER (
            ORDER BY SaleMonth
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        )
    , 2)                                                              AS Rolling3MonthAvg
FROM MonthlySales
ORDER BY SaleMonth;
