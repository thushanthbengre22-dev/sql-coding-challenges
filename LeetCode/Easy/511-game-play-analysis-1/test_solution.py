import sqlite3
import pytest

SOLUTION = """
SELECT player_id, MIN(event_date) AS first_login
FROM Activity
GROUP BY player_id
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
    result = {row for row in db.execute(SOLUTION)}
    assert result == {(1, "2016-03-01"), (2, "2017-06-25"), (3, "2016-03-02")}


def test_single_player_multiple_dates(db):
    db.executemany("INSERT INTO Activity VALUES (?,?,?,?)", [
        (1, 1, "2020-01-05", 3),
        (1, 1, "2020-01-01", 1),
        (1, 1, "2020-01-10", 7),
    ])
    result = list(db.execute(SOLUTION))
    assert result == [(1, "2020-01-01")]


def test_each_player_single_login(db):
    db.executemany("INSERT INTO Activity VALUES (?,?,?,?)", [
        (1, 1, "2021-06-01", 0),
        (2, 2, "2021-06-02", 0),
    ])
    result = {row for row in db.execute(SOLUTION)}
    assert result == {(1, "2021-06-01"), (2, "2021-06-02")}


def test_first_login_is_minimum_date(db):
    db.executemany("INSERT INTO Activity VALUES (?,?,?,?)", [
        (1, 1, "2022-12-31", 2),
        (1, 1, "2022-01-01", 9),
        (1, 1, "2022-06-15", 4),
    ])
    result = list(db.execute(SOLUTION))
    assert result == [(1, "2022-01-01")]
