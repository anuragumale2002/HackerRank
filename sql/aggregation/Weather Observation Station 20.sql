SELECT ROUND(AVG(x.LAT_N), 4)
FROM (
    SELECT s.LAT_N, @rn := @rn + 1 AS rn
    FROM STATION s
    JOIN (SELECT @rn := 0) init
    ORDER BY s.LAT_N
) x
JOIN (SELECT COUNT(*) AS n FROM STATION) c
WHERE x.rn IN (FLOOR((c.n + 1) / 2), FLOOR((c.n + 2) / 2));
