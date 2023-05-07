CREATE DATABASE IF NOT EXISTS TetrisDB;
USE TetrisDB;

CREATE TABLE IF NOT EXISTS Teams (
    TeamID VARCHAR(8),
    
    Name TINYTEXT,
    Avg_Score DECIMAL(9,3) DEFAULT 0,
    Trials_Submitted INT CHECK(Trials_Submitted BETWEEN 0 AND 10) DEFAULT 0,
    Began_trial BOOL DEFAULT FALSE,

    CONSTRAINT pk_Teams PRIMARY KEY (TeamID)
);

CREATE TABLE IF NOT EXISTS Trials (
    TeamID VARCHAR(8),
    Trial INT CHECK(Trial BETWEEN 1 AND 10) AUTO_INCREMENT,

    Score INT CHECK(Score >= 0),
    Lines_cleared INT,

    CONSTRAINT pk_Trials PRIMARY KEY (TeamID, Trial),
    CONSTRAINT fk_Teams FOREIGN KEY (TeamID) REFERENCES Teams (TeamID)
)