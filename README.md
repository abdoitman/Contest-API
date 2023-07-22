# Contest API
This repository contains the API responsible for receiving server submissions, evaluating, and storing scores from the **[Tetris Competition](https://github.com/abdoitman/Tetris-Competition)**. 

<hr>

## Server API
[server_api.py](https://github.com/abdoitman/Contest-API/blob/main/server_api.py) file contains the API used to *receive* and *send* HTML to each participant in the competition. The API was created using **FastAPI** and deployed locally using **uvicorn**. To run the API *locally* run:
```console
uvicorn server_api:app --reload
```
### Game Seeds
To ensure a fair game among all teams, a series of random numbers with a fixed seed are generated each time a team tries to play a game. Each of these random numbers will later be used as a random seed for each game to ensure that all teams play at most 10 **random** games and **all teams** play the **same** 10 random games. <br>

*For example:* if Team A have played 4 games on the server already, then their next game seed will be the fifth in the list, while Team B is on the second seed because they played only one time before. <br>

<p align=center> <img src="https://github.com/abdoitman/Contest-API/assets/77892920/3bcfc3ab-8aec-4a72-9126-5cd6073093ee"> </p>

### API
The API consists of **2 GET** requests and **1 POST** request: <br>

  * `.../submit/{team_id}` :
    * At the start of each server submission, any participating team should send this **GET** request to the API to the random seed of the current trial they're on.
    * **NOTE:** This request is sent automatically when a team starts a server submission <br>
  * `.../info/{team_id}` :
    * Any team can access their information at any time using this **GET** request. Their info will contain their **average score, number of submitted trials, and the score of each past trial**
  * `.../finish/{team_id}/` : 
    * At the end of each server submission, the game sends the necessary information to the API using this **POST** request to calculate the score and validate the integrity of the game files on the team's PC. Then, it stores the trial information in the database.
    * **NOTE:** This request is sent automatically when a team starts a server submission <br>

<p align=center> <img src="https://github.com/abdoitman/Contest-API/assets/77892920/8f09b811-0310-4e01-9a2d-ec716071b169"> </p>
<hr>

## Functions
The [functions.py](https://github.com/abdoitman/Contest-API/blob/main/functions.py) file contains the necessary functions to communicate between the API and the database, which are:<br>
  * `connect_to_database` : opens the connection to the database.
  * `set_begin_flag` : sets up a boolean in the database that marks that the team has started a trial.
  * `began_trial` : check if a team has already started a trial and hasn't completed it yet.
  * `get_teams` : returns the current teams from the database.
  * `insert_trial` : inserts a new trial in the DB.
  * `get_seed` : gets the index at which a team should pull the seed from the list of seeds upon.
  * `get_trials_submitted` : gets the total number of submissions so far for any team.
  * `fetch_team_info` : gets the team info.

Also, it contains 2 other functions: <br>
  * `check_cheating` : checks if the submitting team has altered the game files.
  * `calculate_score` : calculate the score of the submitted trial based on the number of cleared lines and the level. 

<hr>

## SQL
In [sql folder](https://github.com/abdoitman/Contest-API/tree/main/sql) lies 2 SQL scripts related to the [creation of the database](https://github.com/abdoitman/Contest-API/blob/main/sql/create_database.sql) and the [creation of the triggers](https://github.com/abdoitman/Contest-API/blob/main/sql/database_logic.sql) in the database. <br>

See the documentation [here](https://github.com/abdoitman/Contest-API/tree/main/sql).
