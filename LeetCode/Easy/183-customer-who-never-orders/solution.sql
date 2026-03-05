SELECT name AS Customers
FROM Customers
WHERE id NOT IN
      (SELECT c.id FROM Customers c INNER JOIN Orders o ON o.customerId = c.id);