WITH MaxSalaries AS (SELECT departmentId, MAX(salary) AS max_salary
                     FROM Employee
                     GROUP BY departmentId)
SELECT d.name AS Department, e.name AS Employee, e.salary AS Salary
FROM Employee e
         INNER JOIN Department d ON d.id = e.departmentId
         INNER JOIN MaxSalaries m ON m.departmentId = e.departmentId
    AND e.salary = m.max_salary
ORDER BY d.name;