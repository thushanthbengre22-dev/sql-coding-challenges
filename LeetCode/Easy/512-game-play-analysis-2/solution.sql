WITH FirstLogin AS
         (SELECT player_id, device_id, MIN(event_date) as first_login
          FROM Activity
          GROUP BY player_id
         )
SELECT a.player_id, a.device_id
FROM Activity a
         INNER JOIN FirstLogin fl on fl.player_id = a.player_id
    AND a.event_date = fl.first_login;
