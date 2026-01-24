SELECT f1.X, f1.Y
FROM Functions f1
JOIN Functions f2
  ON f1.X = f2.Y
 AND f1.Y = f2.X
WHERE f1.X < f1.Y
   OR (f1.X = f1.Y AND f1.X IN (
        SELECT X
        FROM Functions
        WHERE X = Y
        GROUP BY X
        HAVING COUNT(*) > 1
   ))
GROUP BY f1.X, f1.Y
ORDER BY f1.X;
