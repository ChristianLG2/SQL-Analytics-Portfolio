USE Northwind;
GO

WITH FirstPurchase AS (
    SELECT
        CustomerID,
        DATEFROMPARTS(YEAR(MIN(OrderDate)), MONTH(MIN(OrderDate)), 1) AS CohortMonth
    FROM Orders
    WHERE OrderDate IS NOT NULL
    GROUP BY CustomerID
),
CustomerActivity AS (
    SELECT
        fp.CustomerID,
        fp.CohortMonth,
        DATEFROMPARTS(YEAR(o.OrderDate), MONTH(o.OrderDate), 1) AS OrderMonth,
        DATEDIFF(MONTH, fp.CohortMonth,
            DATEFROMPARTS(YEAR(o.OrderDate), MONTH(o.OrderDate), 1)) AS MonthsElapsed
    FROM FirstPurchase fp
    JOIN Orders o ON fp.CustomerID = o.CustomerID
    WHERE o.OrderDate IS NOT NULL
),
CohortSize AS (
    SELECT CohortMonth, COUNT(DISTINCT CustomerID) AS TotalCustomers
    FROM FirstPurchase
    GROUP BY CohortMonth
)
SELECT
    ca.CohortMonth,
    cs.TotalCustomers                                           AS CohortSize,
    ca.MonthsElapsed,
    COUNT(DISTINCT ca.CustomerID)                              AS ActiveCustomers,
    ROUND(100.0 * COUNT(DISTINCT ca.CustomerID)
        / cs.TotalCustomers,2)                               AS RetentionRate
FROM CustomerActivity ca
JOIN CohortSize cs ON ca.CohortMonth = cs.CohortMonth
WHERE ca.MonthsElapsed BETWEEN 0 AND 6
GROUP BY ca.CohortMonth, cs.TotalCustomers, ca.MonthsElapsed
ORDER BY ca.CohortMonth, ca.MonthsElapsed;
