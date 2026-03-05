import sqlite3
import pytest

SOLUTION = """
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
        (1, "Joe", 85000, 1),
        (2, "Henry", 80000, 2),
        (3, "Sam", 60000, 2),
        (4, "Max", 90000, 1),
        (5, "Janet", 69000, 1),
        (6, "Randy", 85000, 1),
        (7, "Will", 70000, 1),
    ])
    result = set(db.execute(SOLUTION).fetchall())
    assert result == {
        ("IT", "Max", 90000),
        ("IT", "Joe", 85000),
        ("IT", "Randy", 85000),
        ("IT", "Will", 70000),
        ("Sales", "Henry", 80000),
        ("Sales", "Sam", 60000),
    }


def test_fewer_than_three_in_department(db):
    db.executemany("INSERT INTO Department VALUES (?,?)", [(1, "IT")])
    db.executemany("INSERT INTO Employee VALUES (?,?,?,?)", [(1, "Alice", 90000, 1), (2, "Bob", 80000, 1)])
    result = set(db.execute(SOLUTION).fetchall())
    assert result == {("IT", "Alice", 90000), ("IT", "Bob", 80000)}


def test_fourth_salary_excluded(db):
    db.executemany("INSERT INTO Department VALUES (?,?)", [(1, "IT")])
    db.executemany("INSERT INTO Employee VALUES (?,?,?,?)", [
        (1, "A", 100000, 1), (2, "B", 90000, 1), (3, "C", 80000, 1), (4, "D", 70000, 1),
    ])
    result = {row[1] for row in db.execute(SOLUTION)}
    assert "D" not in result
    assert result == {"A", "B", "C"}


def test_ties_within_top_three_all_included(db):
    # Two employees tied at rank 2 — both should appear, and rank 3 still counts
    db.executemany("INSERT INTO Department VALUES (?,?)", [(1, "IT")])
    db.executemany("INSERT INTO Employee VALUES (?,?,?,?)", [
        (1, "A", 100000, 1), (2, "B", 90000, 1), (3, "C", 90000, 1), (4, "D", 80000, 1),
    ])
    result = {row[1] for row in db.execute(SOLUTION)}
    assert result == {"A", "B", "C", "D"}


def test_empty_employee_table(db):
    db.execute("INSERT INTO Department VALUES (1, 'IT')")
    result = list(db.execute(SOLUTION))
    assert result == []