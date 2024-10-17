-- Write a SQL script that creates a table users following these requirements:
-- If the table already exists, your script should not fail
-- Your script can be executed on any database
SELECT origin AS origin, SUM(fans) AS nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;
