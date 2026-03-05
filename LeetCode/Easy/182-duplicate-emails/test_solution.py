import sqlite3
import pytest

SOLUTION = """
SELECT email
FROM Person
GROUP BY email
HAVING COUNT(email) > 1
"""


@pytest.fixture
def db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE Person (id INT PRIMARY KEY, email TEXT)")
    yield conn
    conn.close()


def test_example(db):
    db.executemany("INSERT INTO Person VALUES (?,?)", [(1, "a@b.com"), (2, "c@d.com"), (3, "a@b.com")])
    result = {row[0] for row in db.execute(SOLUTION)}
    assert result == {"a@b.com"}


def test_no_duplicates_returns_empty(db):
    db.executemany("INSERT INTO Person VALUES (?,?)", [(1, "a@b.com"), (2, "c@d.com")])
    result = list(db.execute(SOLUTION))
    assert result == []


def test_multiple_duplicates(db):
    db.executemany("INSERT INTO Person VALUES (?,?)", [
        (1, "a@b.com"), (2, "a@b.com"),
        (3, "x@y.com"), (4, "x@y.com"),
        (5, "unique@z.com"),
    ])
    result = {row[0] for row in db.execute(SOLUTION)}
    assert result == {"a@b.com", "x@y.com"}


def test_all_same_email(db):
    db.executemany("INSERT INTO Person VALUES (?,?)", [(1, "same@x.com"), (2, "same@x.com"), (3, "same@x.com")])
    result = {row[0] for row in db.execute(SOLUTION)}
    assert result == {"same@x.com"}