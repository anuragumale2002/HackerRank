WITH RECURSIVE nums AS (
    SELECT 20 AS n
    UNION ALL
    SELECT n - 1 FROM nums WHERE n > 1
)
SELECT REPEAT('* ', n)
FROM nums;
