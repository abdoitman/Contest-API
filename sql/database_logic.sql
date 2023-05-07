USE TetrisDB;

DROP TRIGGER IF EXISTS Trials_after_insert;

DELIMITER //

CREATE TRIGGER Trials_after_insert AFTER INSERT ON Trials
FOR EACH ROW
BEGIN
    -- Update the number of trials submitted by the team
    UPDATE Teams
    SET Teams.Trials_Submitted = Teams.Trials_Submitted + 1
    WHERE Teams.TeamID = NEW.TeamID;

	-- Set the flag back to false
	UPDATE Teams
    SET Teams.Began_trial = False
    WHERE Teams.TeamID = NEW.TeamID;

    -- Update the score to be equal to the average of the top 3 submissions
	UPDATE Teams
    SET Avg_Score = (
		SELECT Avg(Score)
        FROM (
			SELECT Score
            FROM Trials
            WHERE TeamID = NEW.TeamID
            ORDER BY Score DESC
            LIMIT 3
        ) AS TOP_3
    )
    WHERE Teams.TeamID = NEW.TeamID;	
END//

DELIMITER ;