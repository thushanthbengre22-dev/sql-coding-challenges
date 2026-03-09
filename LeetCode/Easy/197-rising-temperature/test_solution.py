import sqlite3
import pytest

# Note: DATEDIFF is MySQL-specific; using julianday() for SQLite compatibility
SOLUTION = """
SELECT w.id
FROM Weather w
         JOIN Weather w2 ON julianday(w.recordDate) - julianday(w2.recordDate) = 1
WHERE w.temperature > w2.temperature
"""


@pytest.fixture
def db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE Weather (id INT PRIMARY KEY, recordDate TEXT, temperature INT)")
    yield conn
    conn.close()


def test_example(db):
    db.executemany("INSERT INTO Weather VALUES (?,?,?)", [
        (1, "2015-01-01", 10),
        (2, "2015-01-02", 25),
        (3, "2015-01-03", 20),
        (4, "2015-01-04", 30),
    ])
    result = {row[0] for row in db.execute(SOLUTION)}
    assert result == {2, 4}


def test_no_warmer_day(db):
    db.executemany("INSERT INTO Weather VALUES (?,?,?)", [
        (1, "2015-01-01", 30),
        (2, "2015-01-02", 20),
        (3, "2015-01-03", 10),
    ])
    result = list(db.execute(SOLUTION))
    assert result == []


def test_all_warmer(db):
    db.executemany("INSERT INTO Weather VALUES (?,?,?)", [
        (1, "2015-01-01", 10),
        (2, "2015-01-02", 20),
        (3, "2015-01-03", 30),
    ])
    result = {row[0] for row in db.execute(SOLUTION)}
    assert result == {2, 3}


def test_same_temperature_not_included(db):
    db.executemany("INSERT INTO Weather VALUES (?,?,?)", [
        (1, "2015-01-01", 15),
        (2, "2015-01-02", 15),
    ])
    result = list(db.execute(SOLUTION))
    assert result == []


def test_single_row(db):
    db.execute("INSERT INTO Weather VALUES (1, '2015-01-01', 10)")
    result = list(db.execute(SOLUTION))
    assert result == []
