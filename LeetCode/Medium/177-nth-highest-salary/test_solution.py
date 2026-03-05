import sqlite3
import pytest

# The original solution is a MySQL stored function. Since SQLite doesn't support
# that syntax, we test the equivalent core query logic directly.
def nth_highest_salary(conn, n):
    offset = n - 1
    query = f"SELECT DISTINCT salary FROM Employee ORDER BY salary DESC LIMIT 1 OFFSET {offset}"
    row = conn.execute(query).fetchone()
    return row[0] if row else None


@pytest.fixture
def db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE Employee (id INT PRIMARY KEY, salary INT)")
    yield conn
    conn.close()


def test_second_highest(db):
    db.executemany("INSERT INTO Employee VALUES (?,?)", [(1, 100), (2, 200), (3, 300)])
    assert nth_highest_salary(db, 2) == 200


def test_n_exceeds_distinct_salaries_returns_none(db):
    db.execute("INSERT INTO Employee VALUES (1, 100)")
    assert nth_highest_salary(db, 2) is None


def test_first_highest(db):
    db.executemany("INSERT INTO Employee VALUES (?,?)", [(1, 100), (2, 200), (3, 300)])
    assert nth_highest_salary(db, 1) == 300


def test_duplicates_are_ignored(db):
    # 300 is the 1st, 200 is the 2nd distinct — duplicate 300s shouldn't affect rank
    db.executemany("INSERT INTO Employee VALUES (?,?)", [(1, 300), (2, 300), (3, 200), (4, 100)])
    assert nth_highest_salary(db, 2) == 200


def test_empty_table_returns_none(db):
    assert nth_highest_salary(db, 1) is None