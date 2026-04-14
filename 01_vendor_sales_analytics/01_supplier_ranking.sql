-- USE Northwind;
-- GO

-- Business Question: Which suppliers drive the most revenue?
-- How does each supplier rank within their product category?

-- In order to give answer to these 2 questions I wrote the following query:


--SELECT s.SupplierID, 
--	s.CompanyName, 
--	SUM(od.Quantity) as total_Quantity, 
--	ROUND(SUM(CAST(od.Quantity * od.UnitPrice * od.Discount AS FLOAT)),2) AS total_discount, 
--	ROUND(SUM((od.UnitPrice * od.Quantity)*(1 - od.Discount)),2) as total_order_revenue
--FROM Suppliers AS s
--	JOIN Products AS p ON p.SupplierID = s.SupplierID
--	JOIN [Order Details] AS od ON p.ProductID = od.ProductID
--GROUP BY s.SupplierID, s.CompanyName
--ORDER BY total_order_revenue DESC;


-- I first selected from the suppliers (s) table PK: SupplierID and CompanyName. By Joining Products (p) ON p.SupplierID = s.SupplierID and [Order Details] AS od ON p.ProductID = od.ProductID I am able to extract od.Quantity, od.UnitPrice and od.Discount and agreggate them for EDA. We also Group By Unagreggate selections SupplierID and CompanyName to display results on distinct ID and company. Finaly we Order By total_order_revenue DESC simulating a Top Ranking.


-- Now I need to transform this first query to CTE and Window functions by
-- 1. Applying RANK() & 2. CAST + ROUND for cleaner Output 

-- Resoning: Easier to write � Each step is simpler, reducing errors during implementation, Easier to read � Others (and future you) can follow the logic, Easier to debug, You can inspect intermediate values to find where things went wrong & The old math advice "Show your work" holds true!


WITH SupplierProducts AS (
    SELECT 
        s.SupplierID,
        s.CompanyName,
        p.ProductID,
		p.CategoryID
    FROM Suppliers s
    JOIN Products p 
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
    JOIN [Order Details] od
        ON sp.ProductID = od.ProductID
	JOIN Categories c
		ON sp.CategoryID = c.CategoryID
),

SupplierTotals AS (
	SELECT 
		SupplierID,
		CompanyName,
		CategoryName,
		SUM(Quantity) AS total_quantity_sold,
		ROUND(SUM(CAST(Quantity * UnitPrice * Discount AS FLOAT)), 2) AS total_discount,
		ROUND(SUM((UnitPrice * Quantity) * (1 - Discount)), 2) AS total_order_revenue
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
