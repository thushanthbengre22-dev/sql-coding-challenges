import sqlite3
import pytest

SOLUTION = """
SELECT name AS Customers
FROM Customers
WHERE id NOT IN
      (SELECT c.id FROM Customers c INNER JOIN Orders o ON o.customerId = c.id)
"""


@pytest.fixture
def db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE Customers (id INT PRIMARY KEY, name TEXT)")
    conn.execute("CREATE TABLE Orders (id INT PRIMARY KEY, customerId INT)")
    yield conn
    conn.close()


def test_example(db):
    db.executemany("INSERT INTO Customers VALUES (?,?)", [(1, "Joe"), (2, "Henry"), (3, "Sam"), (4, "Max")])
    db.executemany("INSERT INTO Orders VALUES (?,?)", [(1, 3), (2, 1)])
    result = {row[0] for row in db.execute(SOLUTION)}
    assert result == {"Henry", "Max"}


def test_all_customers_have_orders(db):
    db.executemany("INSERT INTO Customers VALUES (?,?)", [(1, "Alice"), (2, "Bob")])
    db.executemany("INSERT INTO Orders VALUES (?,?)", [(1, 1), (2, 2)])
    result = list(db.execute(SOLUTION))
    assert result == []


def test_no_orders_returns_all_customers(db):
    db.executemany("INSERT INTO Customers VALUES (?,?)", [(1, "Alice"), (2, "Bob")])
    result = {row[0] for row in db.execute(SOLUTION)}
    assert result == {"Alice", "Bob"}


def test_empty_customers_returns_empty(db):
    result = list(db.execute(SOLUTION))
    assert result == []


def test_customer_with_multiple_orders_excluded_once(db):
    db.executemany("INSERT INTO Customers VALUES (?,?)", [(1, "Alice"), (2, "Bob")])
    db.executemany("INSERT INTO Orders VALUES (?,?)", [(1, 1), (2, 1), (3, 1)])
    result = {row[0] for row in db.execute(SOLUTION)}
    assert result == {"Bob"}