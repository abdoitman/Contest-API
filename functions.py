import random
import collections
import mysql.connector
import os
from dotenv import find_dotenv, load_dotenv

env_file = find_dotenv()
load_dotenv(env_file)

DATABASE = os.environ["DATABASE"]
HOST = os.environ["HOST"]
USER = os.environ["USER"]
PASSWORD = os.environ["PASSWORD"]
PORT = os.environ["PORT"]

random.seed(30)
random_seeds = [random.randint(10, 100) for i in range(10)]
print(random_seeds)

def connect_to_database(database : str):

    conn = mysql.connector.connect(
        host= HOST,
        port= PORT,
        user= USER,
        password= PASSWORD
    )

    cur = conn.cursor()
    cur.execute(f"USE {database};")
    print(f"Connected to {database} successfully!")
    return conn, cur

def set_begin_flag(conn, cur, team_id):
    SQL_command = f"""
    UPDATE Teams
    SET Teams.Begin_trial = True
    WHERE Teams.TeamID = "{team_id}"
    """

    cur.execute(SQL_command)
    conn.commit()

def began_trial(cur, team_id):
    SQL_command = f"""
    SELECT Begin_trial
    FROM Teams
    WHERE TeamID = "{team_id}"
    """
    cur.execute(SQL_command)
    return int(cur.fetchall()[0][0])

def get_teams(cur):
    SQL_command = """
    SELECT TeamID
    FROM Teams;
    """

    cur.execute(SQL_command)

    return [ str(team[0]) for team in cur.fetchall() ]

def insert_trial(conn, cur, team_id: str, trial_number: int, score: int, lines_cleared: int):
    SQL_command = f"""
    INSERT INTO Trials
    VALUES ("{team_id}", {trial_number}, {score}, {lines_cleared});
    """

    cur.execute(SQL_command)
    conn.commit()

def get_seed(cur, team_id : str):
    global random_seeds

    SQL_command = f"""
    SELECT Trials_Submitted
    FROM Teams
    WHERE TeamID = '{team_id}';
    """
    cur.execute(SQL_command)
    team_index = cur.fetchall()[0][0]
    return random_seeds[int(team_index)]

def get_trials_submitted(cur, team_id : str):
    SQL_command = f"""
    SELECT Trials_Submitted
    FROM Teams
    WHERE TeamID = "{team_id}"
    """

    cur.execute(SQL_command)
    return int(cur.fetchall()[0][0])

def terminate_connection(conn) -> None:
    conn.close()

def append_team(conn, cur, team_id : str, name : str):
    SQL_command = f"INSERT INTO Teams (TeamID, Name) Values ('{team_id}' , '{name}');"

    cur.execute(SQL_command)
    conn.commit()

def append_trial(conn, cur, team_id : str, trial_number : int, score : int, lines_cleared : int):
    SQL_command = (f"INSERT INTO Trials Values ('{team_id}' , {trial_number}, {score}, {lines_cleared});")

    cur.execute(SQL_command)
    conn.commit()

def fetch_team_info(cur, team_id : str):
    General_info = f"""
    SELECT *
    FROM Teams
    WHERE TeamID = "{team_id}";
    """

    cur.execute(General_info)
    team_info = {}
    for row in cur.fetchall():
        team_info["TeamID"] = str(row[0])
        team_info["Name"] = str(row[1])
        team_info["Average Score"] = float(row[2])
        team_info["Number of Submitted Trials"] = int(row[3])

    past_trials_details = f"""
    SELECT Trial, Score
    FROM Trials
    WHERE TeamID = "{team_id}"
    """
    cur.execute(past_trials_details)
    past_trials = []
    for row in cur.fetchall():

        past_trial = {
            "Trial" : int(row[0]),
            "Score" : int(row[1])
        }

        past_trials.append(past_trial)

    team_info["Past Trials"] = past_trials
    return team_info

def check_cheating(raw_score: int, raw_lines_cleared: int, raw_counter: list[int], score: int, lines_cleared: int):
    if raw_score != score:
        return True
    elif raw_lines_cleared != lines_cleared:
        return True
    elif any([c / (100*120) > 89 for c in raw_counter]):
        return True
    elif raw_counter != sorted(raw_counter, reverse=True):
        return True
    elif any([c % 120000 for c in raw_counter]):
        return True
            
    return False

def calculate_score(moves: list[int]):
    score = total_lines_cleared = 0
    level = 1
    POINTS_PER_LINE = {
            1 : 800,
            2 : 1200,
            3 : 1800,
            4 : 2000
        }
    moves_lines = dict(collections.Counter(moves))

    for move in sorted(moves_lines.keys()):
        current_move_score = POINTS_PER_LINE[moves_lines[move]]
        total_lines_cleared += moves_lines[move]

        score += current_move_score * level
        level = total_lines_cleared//10 + 1

    return (score, total_lines_cleared)