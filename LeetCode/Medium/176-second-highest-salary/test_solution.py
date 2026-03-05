import sqlite3
import pytest

SOLUTION = """
SELECT MAX(salary) AS SecondHighestSalary
FROM Employee
WHERE salary < (SELECT MAX(salary) FROM Employee)
"""


@pytest.fixture
def db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE Employee (id INT PRIMARY KEY, salary INT)")
    yield conn
    conn.close()


def test_example(db):
    db.executemany("INSERT INTO Employee VALUES (?,?)", [(1, 100), (2, 200), (3, 300)])
    result = db.execute(SOLUTION).fetchone()[0]
    assert result == 200


def test_single_row_returns_null(db):
    db.execute("INSERT INTO Employee VALUES (1, 100)")
    result = db.execute(SOLUTION).fetchone()[0]
    assert result is None


def test_all_same_salary_returns_null(db):
    db.executemany("INSERT INTO Employee VALUES (?,?)", [(1, 100), (2, 100), (3, 100)])
    result = db.execute(SOLUTION).fetchone()[0]
    assert result is None


def test_two_distinct_salaries(db):
    db.executemany("INSERT INTO Employee VALUES (?,?)", [(1, 500), (2, 300)])
    result = db.execute(SOLUTION).fetchone()[0]
    assert result == 300


def test_empty_table_returns_null(db):
    result = db.execute(SOLUTION).fetchone()[0]
    assert result is None