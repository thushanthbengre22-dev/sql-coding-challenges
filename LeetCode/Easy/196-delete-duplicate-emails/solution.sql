DELETE FROM Person
WHERE id NOT IN (
    SELECT id FROM(
                      SELECT MIN(id) as id
                      from Person
                      GROUP BY email
                  ) AS temp
);