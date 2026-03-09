# Game Play Analysis III

## Problem Description

Table: `Activity`

| Column Name  | Type |
|--------------|------|
| player_id    | int  |
| device_id    | int  |
| event_date   | date |
| games_played | int  |

`(player_id, event_date)` is the primary key for this table.
This table shows the activity of players of some games.
Each row is a record of a player who logged in and played a number of games (possibly 0) before logging out on that day using that device.

Write a solution to find for each player and date, how many **games played so far** by the player. That is, the total number of games played by the player until that date. Check the example for clarity.

Return the result table in any order.

## Example 1

**Input:**

`Activity` table:

| player_id | device_id | event_date | games_played |
|-----------|-----------|------------|--------------|
| 1         | 2         | 2016-03-01 | 5            |
| 1         | 2         | 2016-05-02 | 6            |
| 2         | 3         | 2017-06-25 | 1            |
| 3         | 1         | 2016-03-02 | 0            |
| 3         | 4         | 2018-07-03 | 5            |

**Output:**

| player_id | event_date | games_played_so_far |
|-----------|------------|---------------------|
| 1         | 2016-03-01 | 5                   |
| 1         | 2016-05-02 | 11                  |
| 2         | 2017-06-25 | 1                   |
| 3         | 2016-03-02 | 0                   |
| 3         | 2018-07-03 | 5                   |

**Explanation:**
For player 1, the running total on 2016-03-01 is 5, and on 2016-05-02 it accumulates to 5 + 6 = 11.
