import sqlite3
import pytest

# Note: Window functions require SQLite 3.25.0+
SOLUTION = """
SELECT player_id, event_date,
       SUM(games_played) OVER (
    PARTITION BY player_id
    ORDER BY event_date
) AS games_played_so_far
FROM Activity
ORDER BY player_id, event_date
"""


@pytest.fixture
def db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE Activity (player_id INT, device_id INT, event_date TEXT, games_played INT, PRIMARY KEY (player_id, event_date))")
    yield conn
    conn.close()


def test_example(db):
    db.executemany("INSERT INTO Activity VALUES (?,?,?,?)", [
        (1, 2, "2016-03-01", 5),
        (1, 2, "2016-05-02", 6),
        (2, 3, "2017-06-25", 1),
        (3, 1, "2016-03-02", 0),
        (3, 4, "2018-07-03", 5),
    ])
    result = db.execute(SOLUTION).fetchall()
    assert result == [
        (1, "2016-03-01", 5),
        (1, "2016-05-02", 11),
        (2, "2017-06-25", 1),
        (3, "2016-03-02", 0),
        (3, "2018-07-03", 5),
    ]


def test_single_player_cumulative(db):
    db.executemany("INSERT INTO Activity VALUES (?,?,?,?)", [
        (1, 1, "2021-01-01", 3),
        (1, 1, "2021-01-02", 7),
        (1, 1, "2021-01-03", 2),
    ])
    result = db.execute(SOLUTION).fetchall()
    assert result == [
        (1, "2021-01-01", 3),
        (1, "2021-01-02", 10),
        (1, "2021-01-03", 12),
    ]


def test_players_partitioned_independently(db):
    db.executemany("INSERT INTO Activity VALUES (?,?,?,?)", [
        (1, 1, "2022-01-01", 10),
        (2, 2, "2022-01-01", 5),
        (1, 1, "2022-01-02", 3),
        (2, 2, "2022-01-02", 4),
    ])
    result = db.execute(SOLUTION).fetchall()
    assert result == [
        (1, "2022-01-01", 10),
        (1, "2022-01-02", 13),
        (2, "2022-01-01", 5),
        (2, "2022-01-02", 9),
    ]


def test_zero_games_played(db):
    db.executemany("INSERT INTO Activity VALUES (?,?,?,?)", [
        (1, 1, "2020-05-01", 0),
        (1, 1, "2020-05-02", 0),
    ])
    result = db.execute(SOLUTION).fetchall()
    assert result == [(1, "2020-05-01", 0), (1, "2020-05-02", 0)]


def test_single_row(db):
    db.execute("INSERT INTO Activity VALUES (1, 1, '2023-01-01', 42)")
    result = db.execute(SOLUTION).fetchall()
    assert result == [(1, "2023-01-01", 42)]
