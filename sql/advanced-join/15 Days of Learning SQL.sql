SELECT sd, cnt, h.hacker_id, h.name
FROM(

SELECT sd, (SELECT COUNT(DISTINCT h.hacker_id) FROM hackers h JOIN submissions s ON s.hacker_id = h.hacker_id WHERE s.submission_date <= sd AND
            (SELECT COUNT(DISTINCT submission_date) FROM hackers hh JOIN submissions ss ON ss.hacker_id = hh.hacker_id WHERE hh.hacker_id = h.hacker_id
            AND ss.submission_date <= sd
            )
            = 1+DATEDIFF(sd,'2016-03-01')) AS cnt,
(SELECT h.hacker_id FROM hackers h JOIN submissions s ON s.hacker_id = h.hacker_id WHERE s.submission_date = sd GROUP BY h.hacker_id ORDER BY COUNT(s.submission_id) DESC, h.hacker_id LIMIT 1) AS hacker_id,
    (SELECT COUNT(s.submission_id) FROM hackers h JOIN submissions s ON s.hacker_id = h.hacker_id WHERE s.submission_date = sd GROUP BY h.hacker_id ORDER BY COUNT(s.submission_id) DESC, h.hacker_id LIMIT 1) AS hacker_cnt

FROM
    (SELECT submission_date sd
     FROM submissions
     GROUP BY submission_date
    ) AS date_tbl

) AS TBL2
JOIN hackers h ON h.hacker_id = TBL2.hacker_id
ORDER BY sd