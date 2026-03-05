import sqlite3
import pytest

SOLUTION = """
WITH MaxSalaries AS (SELECT departmentId, MAX(salary) AS max_salary
                     FROM Employee
                     GROUP BY departmentId)
SELECT d.name AS Department, e.name AS Employee, e.salary AS Salary
FROM Employee e
         INNER JOIN Department d ON d.id = e.departmentId
         INNER JOIN MaxSalaries m ON m.departmentId = e.departmentId
    AND e.salary = m.max_salary
ORDER BY d.name
"""


@pytest.fixture
def db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE Employee (id INT PRIMARY KEY, name TEXT, salary INT, departmentId INT)")
    conn.execute("CREATE TABLE Department (id INT PRIMARY KEY, name TEXT)")
    yield conn
    conn.close()


def test_example(db):
    db.executemany("INSERT INTO Department VALUES (?,?)", [(1, "IT"), (2, "Sales")])
    db.executemany("INSERT INTO Employee VALUES (?,?,?,?)", [
        (1, "Joe", 70000, 1),
        (2, "Jim", 90000, 1),
        (3, "Henry", 80000, 2),
        (4, "Sam", 60000, 2),
        (5, "Max", 90000, 1),
    ])
    result = set(db.execute(SOLUTION).fetchall())
    assert result == {("IT", "Jim", 90000), ("IT", "Max", 90000), ("Sales", "Henry", 80000)}


def test_single_employee_per_department(db):
    db.executemany("INSERT INTO Department VALUES (?,?)", [(1, "IT"), (2, "Sales")])
    db.executemany("INSERT INTO Employee VALUES (?,?,?,?)", [(1, "Alice", 50000, 1), (2, "Bob", 60000, 2)])
    result = set(db.execute(SOLUTION).fetchall())
    assert result == {("IT", "Alice", 50000), ("Sales", "Bob", 60000)}


def test_all_employees_same_salary_in_department(db):
    db.executemany("INSERT INTO Department VALUES (?,?)", [(1, "IT")])
    db.executemany("INSERT INTO Employee VALUES (?,?,?,?)", [
        (1, "Alice", 70000, 1), (2, "Bob", 70000, 1), (3, "Charlie", 70000, 1),
    ])
    result = set(db.execute(SOLUTION).fetchall())
    assert result == {("IT", "Alice", 70000), ("IT", "Bob", 70000), ("IT", "Charlie", 70000)}


def test_empty_employee_table(db):
    db.execute("INSERT INTO Department VALUES (1, 'IT')")
    result = list(db.execute(SOLUTION))
    assert result == []