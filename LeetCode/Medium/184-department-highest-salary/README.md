# Department Highest Salary

## Problem Description

Table: `Employee`

| Column Name  | Type    |
|--------------|---------|
| id           | int     |
| name         | varchar |
| salary       | int     |
| departmentId | int     |

`id` is the primary key for this table.
`departmentId` is a foreign key referencing `Department.id`.
Each row contains employee information including their department.

Table: `Department`

| Column Name | Type    |
|-------------|---------|
| id          | int     |
| name        | varchar |

`id` is the primary key for this table.
Each row contains the ID and name of a department.

Write a solution to find employees who have the highest salary in each department.

Return the result table in any order.

## Example 1

**Input:**

`Employee` table:

| id | name  | salary | departmentId |
|----|-------|--------|--------------|
| 1  | Joe   | 70000  | 1            |
| 2  | Jim   | 90000  | 1            |
| 3  | Henry | 80000  | 2            |
| 4  | Sam   | 60000  | 2            |
| 5  | Max   | 90000  | 1            |

`Department` table:

| id | name  |
|----|-------|
| 1  | IT    |
| 2  | Sales |

**Output:**

| Department | Employee | Salary |
|------------|----------|--------|
| IT         | Jim      | 90000  |
| IT         | Max      | 90000  |
| Sales      | Henry    | 80000  |

**Explanation:**
Max and Jim both have the highest salary of 90000 in the IT department.
Henry has the highest salary of 80000 in the Sales department.