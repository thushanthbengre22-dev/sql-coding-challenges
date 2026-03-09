WITH DailyTrips AS
         (SELECT t.request_at,
                 COUNT(t.id) AS total_trips,
                 SUM(CASE WHEN t.status != "completed" THEN 1 ELSE 0 END) AS cancelled_trips
          FROM Trips t
                   INNER JOIN Users u ON t.client_id = u.users_id
                   INNER JOIN Users u2 ON t.driver_id = u2.users_id
          WHERE u.banned = 'No'
            AND u2.banned = 'No'
            AND t.request_at BETWEEN '2013-10-01' AND '2013-10-03'
          GROUP BY t.request_at
         )
SELECT request_at AS Day,
ROUND(cancelled_trips/total_trips, 2) AS "Cancellation Rate"
FROM DailyTrips
ORDER BY Day;