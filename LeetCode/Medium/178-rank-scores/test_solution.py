import sqlite3
import pytest

# Note: DENSE_RANK() requires SQLite 3.25.0+ (released 2018)
SOLUTION = """
SELECT score, DENSE_RANK() OVER (ORDER BY score DESC) AS rank
FROM Scores
ORDER BY score DESC
"""


@pytest.fixture
def db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE Scores (id INT PRIMARY KEY, score REAL)")
    yield conn
    conn.close()


def test_example(db):
    db.executemany("INSERT INTO Scores VALUES (?,?)", [
        (1, 3.50), (2, 3.65), (3, 4.00), (4, 3.85), (5, 4.00), (6, 3.65),
    ])
    result = db.execute(SOLUTION).fetchall()
    assert result == [
        (4.00, 1),
        (4.00, 1),
        (3.85, 2),
        (3.65, 3),
        (3.65, 3),
        (3.50, 4),
    ]


def test_all_same_score(db):
    db.executemany("INSERT INTO Scores VALUES (?,?)", [(1, 5.0), (2, 5.0)])
    result = db.execute(SOLUTION).fetchall()
    assert result == [(5.0, 1), (5.0, 1)]


def test_all_distinct_scores(db):
    db.executemany("INSERT INTO Scores VALUES (?,?)", [(1, 1.0), (2, 2.0), (3, 3.0)])
    result = db.execute(SOLUTION).fetchall()
    assert result == [(3.0, 1), (2.0, 2), (1.0, 3)]


def test_single_row(db):
    db.execute("INSERT INTO Scores VALUES (1, 9.99)")
    result = db.execute(SOLUTION).fetchall()
    assert result == [(9.99, 1)]