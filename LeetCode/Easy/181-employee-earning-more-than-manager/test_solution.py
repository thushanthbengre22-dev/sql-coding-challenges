import sqlite3
import pytest

SOLUTION = """
SELECT e.name AS Employee
FROM Employee e
INNER JOIN Employee m ON e.managerId = m.id
WHERE e.salary > m.salary
"""


@pytest.fixture
def db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE Employee (id INT, name TEXT, salary INT, managerId INT)")
    yield conn
    conn.close()


def test_example(db):
    db.executemany("INSERT INTO Employee VALUES (?,?,?,?)", [
        (1, "Joe", 70000, 3),
        (2, "Henry", 80000, 4),
        (3, "Sam", 60000, None),
        (4, "Max", 90000, None),
    ])
    result = {row[0] for row in db.execute(SOLUTION)}
    assert result == {"Joe"}


def test_no_employee_earns_more(db):
    db.executemany("INSERT INTO Employee VALUES (?,?,?,?)", [
        (1, "Alice", 50000, 2),
        (2, "Boss", 90000, None),
    ])
    result = list(db.execute(SOLUTION))
    assert result == []


def test_multiple_employees_earn_more(db):
    db.executemany("INSERT INTO Employee VALUES (?,?,?,?)", [
        (1, "Alice", 80000, 3),
        (2, "Bob", 70000, 3),
        (3, "Charlie", 60000, None),
    ])
    result = {row[0] for row in db.execute(SOLUTION)}
    assert result == {"Alice", "Bob"}


def test_top_level_managers_excluded(db):
    # Managers with no managerId should never appear as employees earning more
    db.executemany("INSERT INTO Employee VALUES (?,?,?,?)", [
        (1, "CEO", 999999, None),
    ])
    result = list(db.execute(SOLUTION))
    assert result == []