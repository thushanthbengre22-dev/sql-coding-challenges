import sqlite3
import pytest

SOLUTION = """
SELECT DISTINCT l1.num AS ConsecutiveNums
FROM logs l1
INNER JOIN logs l2 ON l1.id = l2.id - 1
INNER JOIN logs l3 ON l1.id = l3.id - 2
WHERE l1.num = l2.num AND l2.num = l3.num
"""


@pytest.fixture
def db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE logs (id INT PRIMARY KEY, num TEXT)")
    yield conn
    conn.close()


def test_example(db):
    db.executemany("INSERT INTO logs VALUES (?,?)", [
        (1, "1"), (2, "1"), (3, "1"), (4, "2"), (5, "1"), (6, "2"), (7, "2"),
    ])
    result = {row[0] for row in db.execute(SOLUTION)}
    assert result == {"1"}


def test_no_consecutive_numbers(db):
    db.executemany("INSERT INTO logs VALUES (?,?)", [(1, "1"), (2, "2"), (3, "1")])
    result = list(db.execute(SOLUTION))
    assert result == []


def test_multiple_consecutive_numbers(db):
    db.executemany("INSERT INTO logs VALUES (?,?)", [
        (1, "1"), (2, "1"), (3, "1"),
        (4, "2"), (5, "2"), (6, "2"),
    ])
    result = {row[0] for row in db.execute(SOLUTION)}
    assert result == {"1", "2"}


def test_more_than_three_consecutive(db):
    db.executemany("INSERT INTO logs VALUES (?,?)", [
        (1, "5"), (2, "5"), (3, "5"), (4, "5"), (5, "5"),
    ])
    result = {row[0] for row in db.execute(SOLUTION)}
    assert result == {"5"}


def test_exactly_two_consecutive_not_included(db):
    db.executemany("INSERT INTO logs VALUES (?,?)", [(1, "3"), (2, "3"), (3, "9")])
    result = list(db.execute(SOLUTION))
    assert result == []