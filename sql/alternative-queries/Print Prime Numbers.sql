WITH RECURSIVE nums AS (
    SELECT 2 AS n
    UNION ALL
    SELECT n + 1 FROM nums WHERE n < 1000
),
primes AS (
    SELECT n
    FROM nums n1
    WHERE NOT EXISTS (
        SELECT 1
        FROM nums n2
        WHERE n2.n < n1.n
          AND n2.n > 1
          AND n1.n % n2.n = 0
    )
)
SELECT GROUP_CONCAT(n ORDER BY n SEPARATOR '&')
FROM primes;
