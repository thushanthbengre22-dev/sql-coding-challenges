WITH SalaryRanked AS (
    SELECT name, departmentId, salary,
           DENSE_RANK() OVER (PARTITION BY departmentId ORDER BY salary DESC) AS salary_rank
    FROM Employee
),
     TopThree AS (
         SELECT name, salary_rank, departmentId, salary
         FROM SalaryRanked
         WHERE salary_rank BETWEEN 1 AND 3
     )
SELECT d.name as Department, e.name as Employee, e.salary as Salary
from Employee e
         INNER JOIN Department d ON d.id = e.departmentId
         INNER JOIN TopThree t ON t.departmentId = e.departmentId
    AND t.salary = e.salary
    AND e.name = t.name
ORDER BY d.name;

