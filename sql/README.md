# Contest API Database
## Designing The Database
After the normalization of data, the current database design is as follows:
![Database ER](https://github.com/abdoitman/Contest-API/assets/77892920/a29d21c3-d7f3-4b0e-8bdf-6f2f778b2fe2)

<hr>

## Triggers
The database is quite simple, it has only one trigger: **After inserting any trial**, The database automatically does 3 things: <br>
  1. It **increments the number of submitted trials** for the team by one.
  2. It sets the flag of *began_trial* (that indicated that the team has already begun a trial) to **False**.
  3. It **calculate the new average score** of the top 3 scores for the team.
