import sqlite3
import pytest

SOLUTION = """
DELETE FROM Person
WHERE id NOT IN (
    SELECT id FROM(
                      SELECT MIN(id) as id
                      from Person
                      GROUP BY email
                  ) AS temp
)
"""


@pytest.fixture
def db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE Person (id INT PRIMARY KEY, email TEXT)")
    yield conn
    conn.close()


def test_example(db):
    db.executemany("INSERT INTO Person VALUES (?,?)", [
        (1, "john@example.com"), (2, "bob@example.com"), (3, "john@example.com"),
    ])
    db.execute(SOLUTION)
    result = set(db.execute("SELECT id, email FROM Person").fetchall())
    assert result == {(1, "john@example.com"), (2, "bob@example.com")}


def test_no_duplicates_unchanged(db):
    db.executemany("INSERT INTO Person VALUES (?,?)", [(1, "a@b.com"), (2, "c@d.com")])
    db.execute(SOLUTION)
    result = set(db.execute("SELECT id FROM Person").fetchall())
    assert result == {(1,), (2,)}


def test_keeps_smallest_id(db):
    db.executemany("INSERT INTO Person VALUES (?,?)", [(3, "a@b.com"), (1, "a@b.com"), (2, "a@b.com")])
    db.execute(SOLUTION)
    result = db.execute("SELECT id FROM Person").fetchall()
    assert result == [(1,)]


def test_all_same_email_keeps_one(db):
    db.executemany("INSERT INTO Person VALUES (?,?)", [(1, "x@y.com"), (2, "x@y.com"), (3, "x@y.com")])
    db.execute(SOLUTION)
    result = db.execute("SELECT COUNT(*) FROM Person").fetchone()[0]
    assert result == 1


def test_empty_table(db):
    db.execute(SOLUTION)
    result = db.execute("SELECT COUNT(*) FROM Person").fetchone()[0]
    assert result == 0