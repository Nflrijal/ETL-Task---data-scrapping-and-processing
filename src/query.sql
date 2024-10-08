WITH
    winners AS (
        SELECT YEAR, team_name, wins, rank() OVER (
                PARTITION BY
                    YEAR
                ORDER BY wins DESC
            ) AS rk
        FROM data
    ),
    loosers AS (
        SELECT YEAR, team_name, wins, rank() OVER (
                PARTITION BY
                    YEAR
                ORDER BY wins ASC
            ) AS rk
        FROM data
    ),
    combined_cte AS (
        SELECT *, "W" AS identifier
        FROM winners
        WHERE
            rk = 1
        UNION ALL
        SELECT *, "L" AS identifier
        FROM loosers
        WHERE
            rk = 1
        ORDER BY YEAR
    )
SELECT
    YEAR,
    MAX(
        CASE
            WHEN identifier = "W" THEN team_name
        END
    ) AS Winner,
    MAX(
        CASE
            WHEN identifier = "W" THEN wins
        END
    ) AS Winner_Num_of_Wins,
    MAX(
        CASE
            WHEN identifier = "L" THEN team_name
        END
    ) AS Loser,
    MAX(
        CASE
            WHEN identifier = "L" THEN wins
        END
    ) AS Loser_Num_of_Wins
FROM combined_cte
GROUP BY
    YEAR
ORDER BY YEAR