# Contest API Database
## Designing The Database
After the normalization of data, the current database design is as follows:
<p align= "center"><img src="https://github.com/abdoitman/Contest-API/assets/77892920/8cdf889e-8801-4826-afbf-9f3a43a045a6"></p>

<hr>

## Triggers
The database is quite simple, it has only one trigger: `Trials_after_insert` which is executed **after inserting any trial**. The database automatically does 3 things: <br>
  1. It **increments the number of submitted trials** for the team by one.
  2. It sets the flag of *began_trial* (that indicated that the team has already begun a trial) to **False**.
  3. It **calculate the new average score** of the top 3 scores for the team.
