/*
Enter your query here.
*/
SELECT
  h.hacker_id,
  h.name,
  SUM(t.best_score) AS total_score
FROM Hackers h
JOIN (
  SELECT
    hacker_id,
    challenge_id,
    MAX(score) AS best_score
  FROM Submissions
  GROUP BY hacker_id, challenge_id
) t
  ON t.hacker_id = h.hacker_id
GROUP BY h.hacker_id, h.name
HAVING SUM(t.best_score) > 0
ORDER BY total_score DESC, h.hacker_id ASC;
