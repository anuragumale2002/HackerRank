SELECT x.hacker_id, x.name, x.cnt
FROM (
    SELECT h.hacker_id, h.name, COUNT(c.challenge_id) AS cnt
    FROM Hackers h
    JOIN Challenges c
      ON c.hacker_id = h.hacker_id
    GROUP BY h.hacker_id, h.name
) x
WHERE x.cnt = (
    SELECT MAX(cnt)
    FROM (
        SELECT COUNT(*) AS cnt
        FROM Challenges
        GROUP BY hacker_id
    ) m
)
OR x.cnt NOT IN (
    SELECT cnt
    FROM (
        SELECT COUNT(*) AS cnt
        FROM Challenges
        GROUP BY hacker_id
    ) t
    GROUP BY cnt
    HAVING COUNT(*) > 1
)
ORDER BY x.cnt DESC, x.hacker_id ASC;
