import sqlite3
import pytest

# Note: using CAST(... AS REAL) for float division and single quotes for SQLite compatibility
SOLUTION = """
WITH DailyTrips AS
         (SELECT t.request_at,
                 COUNT(t.id) AS total_trips,
                 SUM(CASE WHEN t.status != 'completed' THEN 1 ELSE 0 END) AS cancelled_trips
          FROM Trips t
                   INNER JOIN Users u ON t.client_id = u.users_id
                   INNER JOIN Users u2 ON t.driver_id = u2.users_id
          WHERE u.banned = 'No'
            AND u2.banned = 'No'
            AND t.request_at BETWEEN '2013-10-01' AND '2013-10-03'
          GROUP BY t.request_at
         )
SELECT request_at AS Day,
       ROUND(CAST(cancelled_trips AS REAL) / total_trips, 2) AS 'Cancellation Rate'
FROM DailyTrips
ORDER BY Day
"""


@pytest.fixture
def db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE Trips (id INT PRIMARY KEY, client_id INT, driver_id INT, city_id INT, status TEXT, request_at TEXT)")
    conn.execute("CREATE TABLE Users (users_id INT PRIMARY KEY, banned TEXT, role TEXT)")
    yield conn
    conn.close()


def test_example(db):
    db.executemany("INSERT INTO Users VALUES (?,?,?)", [
        (1, "No", "client"), (2, "Yes", "client"), (3, "No", "client"), (4, "No", "client"),
        (10, "No", "driver"), (11, "No", "driver"), (12, "No", "driver"), (13, "No", "driver"),
    ])
    db.executemany("INSERT INTO Trips VALUES (?,?,?,?,?,?)", [
        (1, 1, 10, 1, "completed", "2013-10-01"),
        (2, 2, 11, 1, "cancelled_by_driver", "2013-10-01"),
        (3, 3, 12, 6, "completed", "2013-10-01"),
        (4, 4, 13, 6, "cancelled_by_client", "2013-10-01"),
        (5, 1, 10, 1, "completed", "2013-10-02"),
        (6, 2, 11, 6, "completed", "2013-10-02"),
        (7, 3, 12, 6, "completed", "2013-10-02"),
        (8, 2, 12, 12, "completed", "2013-10-03"),
        (9, 3, 10, 12, "completed", "2013-10-03"),
        (10, 4, 13, 12, "cancelled_by_driver", "2013-10-03"),
    ])
    result = db.execute(SOLUTION).fetchall()
    assert result == [("2013-10-01", 0.33), ("2013-10-02", 0.0), ("2013-10-03", 0.5)]


def test_all_trips_cancelled(db):
    db.executemany("INSERT INTO Users VALUES (?,?,?)", [
        (1, "No", "client"), (10, "No", "driver"),
    ])
    db.executemany("INSERT INTO Trips VALUES (?,?,?,?,?,?)", [
        (1, 1, 10, 1, "cancelled_by_client", "2013-10-01"),
        (2, 1, 10, 1, "cancelled_by_driver", "2013-10-02"),
    ])
    result = db.execute(SOLUTION).fetchall()
    assert result == [("2013-10-01", 1.0), ("2013-10-02", 1.0)]


def test_no_trips_cancelled(db):
    db.executemany("INSERT INTO Users VALUES (?,?,?)", [
        (1, "No", "client"), (10, "No", "driver"),
    ])
    db.executemany("INSERT INTO Trips VALUES (?,?,?,?,?,?)", [
        (1, 1, 10, 1, "completed", "2013-10-01"),
        (2, 1, 10, 1, "completed", "2013-10-02"),
    ])
    result = db.execute(SOLUTION).fetchall()
    assert result == [("2013-10-01", 0.0), ("2013-10-02", 0.0)]


def test_banned_users_excluded(db):
    db.executemany("INSERT INTO Users VALUES (?,?,?)", [
        (1, "Yes", "client"), (2, "No", "client"),
        (10, "No", "driver"), (11, "Yes", "driver"),
    ])
    db.executemany("INSERT INTO Trips VALUES (?,?,?,?,?,?)", [
        (1, 1, 10, 1, "cancelled_by_client", "2013-10-01"),  # banned client → excluded
        (2, 2, 11, 1, "cancelled_by_driver", "2013-10-01"),  # banned driver → excluded
        (3, 2, 10, 1, "completed", "2013-10-01"),             # both unbanned → included
    ])
    result = db.execute(SOLUTION).fetchall()
    assert result == [("2013-10-01", 0.0)]


def test_trips_outside_date_range_excluded(db):
    db.executemany("INSERT INTO Users VALUES (?,?,?)", [
        (1, "No", "client"), (10, "No", "driver"),
    ])
    db.executemany("INSERT INTO Trips VALUES (?,?,?,?,?,?)", [
        (1, 1, 10, 1, "cancelled_by_client", "2013-09-30"),  # before range
        (2, 1, 10, 1, "completed", "2013-10-04"),             # after range
        (3, 1, 10, 1, "completed", "2013-10-01"),             # in range
    ])
    result = db.execute(SOLUTION).fetchall()
    assert result == [("2013-10-01", 0.0)]
