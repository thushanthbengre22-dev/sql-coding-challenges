import sqlite3
import pytest

SOLUTION = """
WITH FirstLogin AS
         (SELECT player_id, device_id, MIN(event_date) as first_login
          FROM Activity
          GROUP BY player_id
         )
SELECT a.player_id, a.device_id
FROM Activity a
         INNER JOIN FirstLogin fl on fl.player_id = a.player_id
    AND a.event_date = fl.first_login
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
    assert result == {(1, 2), (2, 3), (3, 1)}


def test_single_session_per_player(db):
    db.executemany("INSERT INTO Activity VALUES (?,?,?,?)", [
        (1, 5, "2020-01-01", 3),
        (2, 7, "2020-01-02", 1),
    ])
    result = {row for row in db.execute(SOLUTION)}
    assert result == {(1, 5), (2, 7)}


def test_later_session_device_not_returned(db):
    db.executemany("INSERT INTO Activity VALUES (?,?,?,?)", [
        (1, 10, "2021-01-01", 2),
        (1, 99, "2021-06-01", 4),
    ])
    result = list(db.execute(SOLUTION))
    assert result == [(1, 10)]


def test_multiple_players_correct_devices(db):
    db.executemany("INSERT INTO Activity VALUES (?,?,?,?)", [
        (1, 1, "2022-03-01", 0),
        (1, 2, "2022-03-10", 5),
        (2, 3, "2022-03-05", 1),
        (2, 4, "2022-03-15", 2),
    ])
    result = {row for row in db.execute(SOLUTION)}
    assert result == {(1, 1), (2, 3)}
