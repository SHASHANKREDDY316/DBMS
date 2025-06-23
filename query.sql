SELECT DISTINCT cu.CustomerID, cu.Name
FROM customers cu
JOIN sales s ON cu.CustomerID = s.CustomerID
WHERE cu.CustomerID NOT IN (
    SELECT CustomerID FROM services
);

SELECT 
    MONTH(s.Date) AS Month,
    SUM(s.Amount) AS SalesRevenue,
    (
        SELECT SUM(sv.Cost)
        FROM services sv
        WHERE MONTH(sv.ServiceDate) = MONTH(s.Date)
    ) AS ServiceRevenue
FROM sales s
GROUP BY MONTH(s.Date);

SELECT c.Color, COUNT(*) AS SoldCount
FROM cars c
JOIN sales s ON c.CarID = s.CarID
GROUP BY c.Color
ORDER BY SoldCount DESC
LIMIT 3;

SELECT sv.*
FROM services sv
WHERE (sv.CustomerID, sv.CarID) NOT IN (
    SELECT CustomerID, CarID FROM sales
);

SELECT sv.ServiceID, cu.Name AS CustomerName, c.Model AS CarModel, sv.Cost
FROM services sv
JOIN customers cu ON sv.CustomerID = cu.CustomerID
JOIN cars c ON sv.CarID = c.CarID
WHERE sv.Cost > 5000;
