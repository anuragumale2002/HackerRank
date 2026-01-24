SELECT
  c.company_code,
  c.founder,
  COUNT(DISTINCT lm.lead_manager_code),
  COUNT(DISTINCT sm.senior_manager_code),
  COUNT(DISTINCT m.manager_code),
  COUNT(DISTINCT e.employee_code)
FROM Company c
LEFT JOIN Lead_Manager lm
  ON lm.company_code = c.company_code
LEFT JOIN Senior_Manager sm
  ON sm.company_code = c.company_code
LEFT JOIN Manager m
  ON m.company_code = c.company_code
LEFT JOIN Employee e
  ON e.company_code = c.company_code
GROUP BY c.company_code, c.founder
ORDER BY c.company_code;
