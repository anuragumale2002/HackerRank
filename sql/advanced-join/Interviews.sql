SELECT
  c.contest_id,
  c.hacker_id,
  c.name,
  SUM(ss.total_submissions) AS total_submissions,
  SUM(ss.total_accepted_submissions) AS total_accepted_submissions,
  SUM(vs.total_views) AS total_views,
  SUM(vs.total_unique_views) AS total_unique_views
FROM Contests c
JOIN Colleges co
  ON co.contest_id = c.contest_id
JOIN Challenges ch
  ON ch.college_id = co.college_id
LEFT JOIN (
  SELECT
    challenge_id,
    SUM(total_submissions) AS total_submissions,
    SUM(total_accepted_submissions) AS total_accepted_submissions
  FROM Submission_Stats
  GROUP BY challenge_id
) ss
  ON ss.challenge_id = ch.challenge_id
LEFT JOIN (
  SELECT
    challenge_id,
    SUM(total_views) AS total_views,
    SUM(total_unique_views) AS total_unique_views
  FROM View_Stats
  GROUP BY challenge_id
) vs
  ON vs.challenge_id = ch.challenge_id
GROUP BY c.contest_id, c.hacker_id, c.name
HAVING
  SUM(COALESCE(ss.total_submissions, 0)) +
  SUM(COALESCE(ss.total_accepted_submissions, 0)) +
  SUM(COALESCE(vs.total_views, 0)) +
  SUM(COALESCE(vs.total_unique_views, 0)) > 0
ORDER BY c.contest_id;
