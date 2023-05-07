from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from functions import *

app = FastAPI()

class RawTrial(BaseModel):
    M: list[int]
    S: int
    LC: int
    C: list[int]

conn, cur = connect_to_database(DATABASE)
team_IDs = get_teams(cur)
terminate_connection(conn)

@app.get('/submit/{team_id}')
async def begin(team_id: str):
    if team_id not in team_IDs:
        return HTTPException(status_code=404, detail= f"Team ID ({team_id}) does not exsist!")
    else:
        conn, cur = connect_to_database(DATABASE)
        set_begin_flag(conn, cur, team_id)
        trials_submitted = get_trials_submitted(cur, team_id)
        terminate_connection(conn)
        if trials_submitted == 10:
            return HTTPException(status_code=401, detail= f"Your team ({team_id}) can no more submit to the server!")
 
    conn, cur = connect_to_database(DATABASE)
    seed = get_seed(cur, team_id)
    terminate_connection(conn)
    return {"status_code" : 200,
            "seed": seed}
    
#gets team info
@app.get('/info/{team_id}')
async def get_team_info(team_id: str):
    if team_id not in team_IDs:
        return HTTPException(status_code=404, detail= f"Team ID ({team_id}) does not exsist!")
    else:
        conn, cur = connect_to_database(DATABASE)
        team_info = fetch_team_info(cur, team_id)
        terminate_connection(conn)
        return team_info
    
@app.post('/finish/{team_id}/')
async def end_run(team_id: str, raw_trial: RawTrial):
    if team_id not in team_IDs:
        return HTTPException(status_code=404, detail= f"Team ID ({team_id}) does not exsist!")
    else:
        score, lines_cleared = calculate_score(raw_trial.M)
        if check_cheating(raw_trial.S, raw_trial.LC, raw_trial.C, score, lines_cleared):
            return HTTPException(status_code=401, detail=f"Team {team_id} changed in the game files!")
        else:
            conn, cur = connect_to_database(DATABASE)
            if not began_trial(cur, team_id):
                return HTTPException(status_code= 401, detail="Can't submit a trial without [begin()]")
            trial_number = get_trials_submitted(cur, team_id) + 1
            insert_trial(conn, cur, team_id, trial_number, score, lines_cleared)
            terminate_connection(conn)
            return {"status_code": 200,
                    "response": f"Trial number {trial_number} for {team_id} is accepted!"}
