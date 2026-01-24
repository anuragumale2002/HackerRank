SELECT
  s.Start_Date,
  MIN(e.End_Date) AS End_Date
FROM (
  SELECT Start_Date
  FROM Projects
  WHERE Start_Date NOT IN (SELECT End_Date FROM Projects)
) s
JOIN (
  SELECT End_Date
  FROM Projects
  WHERE End_Date NOT IN (SELECT Start_Date FROM Projects)
) e
  ON e.End_Date > s.Start_Date
GROUP BY s.Start_Date
ORDER BY DATEDIFF(MIN(e.End_Date), s.Start_Date), s.Start_Date;
