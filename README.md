# Contest API
This repository containts the API responsible for recieving server submissions, evaluating, and storing scores from the **[Tetris Competition](https://github.com/abdoitman/Tetris-Competition)**. 

<hr>

## Server API
In [server_api.py](https://github.com/abdoitman/Contest-API/blob/main/server_api.py) file containts the API used to *recieve* and *send* HTML to each participant in the competition. The API was creating using **FastAPI** and deployed locally using **uvicorn**. To run the API *locally* run:
```console
uvicorn server_api:app --reload
```

### Game Seeds
At first to ensure a fair game among all teams, a series of random numbers with a fixed seed are generated in the API that will later be used as a random seed for each game to ensure that all teams play at most 10 **random** games, but **all teams** play the **same** random 10 games. <br>

*For example:* if Team A have played 4 games on the server already, then their next game seed will be the fifth in the list, while Team B is on the second seed because they played only one time before. <br>
![3](https://github.com/abdoitman/Contest-API/assets/77892920/1e43164a-578c-482f-87df-752680333544)

### API
The API consists of **2 GET** requests and **One POST** request: <br>

  * **.../submit/{team_id}** :
    * At the start of each server submission, any participating team should send a GET request to the API to the random seed of the current trial they're on.
    * NOTE: This request is sent automatically when a team starts a server submission <br>
  * **.../info/{team_id}** :
    * Any team can access their information at any time using this GET request. Their info will contain their **average score, number of submitted trials, and the score of each past trial**
  * **.../finish/{team_id}/** : 
    * At the end of each server submission, the game sends the necessary information to the API using this POST request to calculate the score and validate the integrity of the game files on the teams PC. Then, it stores the trial information in the database.
    * NOTE: This request is sent automatically when a team starts a server submission <br>

