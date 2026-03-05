import sqlite3
import pytest

SOLUTION = """
SELECT p.firstName, p.lastName, a.city, a.state
FROM Person p
LEFT JOIN Address a ON p.personId = a.personId
"""


@pytest.fixture
def db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE Person (personId INT, lastName TEXT, firstName TEXT)")
    conn.execute("CREATE TABLE Address (addressId INT, personId INT, city TEXT, state TEXT)")
    yield conn
    conn.close()


def test_example(db):
    db.executemany("INSERT INTO Person VALUES (?,?,?)", [(1, "Wang", "Allen"), (2, "Alice", "Bob")])
    db.executemany("INSERT INTO Address VALUES (?,?,?,?)", [(1, 2, "New York City", "New York")])
    result = set(db.execute(SOLUTION).fetchall())
    assert result == {("Allen", "Wang", None, None), ("Bob", "Alice", "New York City", "New York")}


def test_person_with_no_address_returns_nulls(db):
    db.execute("INSERT INTO Person VALUES (1, 'Smith', 'John')")
    result = db.execute(SOLUTION).fetchall()
    assert result == [("John", "Smith", None, None)]


def test_all_persons_have_address(db):
    db.executemany("INSERT INTO Person VALUES (?,?,?)", [(1, "A", "Alice"), (2, "B", "Bob")])
    db.executemany("INSERT INTO Address VALUES (?,?,?,?)", [
        (1, 1, "Seattle", "WA"),
        (2, 2, "Boston", "MA"),
    ])
    result = set(db.execute(SOLUTION).fetchall())
    assert result == {("Alice", "A", "Seattle", "WA"), ("Bob", "B", "Boston", "MA")}


def test_empty_person_table(db):
    result = db.execute(SOLUTION).fetchall()
    assert result == []