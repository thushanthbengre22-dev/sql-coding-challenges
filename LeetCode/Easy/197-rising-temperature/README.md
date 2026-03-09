# Rising Temperature

## Problem Description

Table: `Weather`

| Column Name | Type |
|-------------|------|
| id          | int  |
| recordDate  | date |
| temperature | int  |

`id` is the primary key for this table.
This table contains information about the temperature on a certain day.

Write a solution to find all dates' `id` with higher temperatures compared to the previous dates (yesterday).

Return the result table in any order.

## Example 1

**Input:**

`Weather` table:

| id | recordDate | temperature |
|----|------------|-------------|
| 1  | 2015-01-01 | 10          |
| 2  | 2015-01-02 | 25          |
| 3  | 2015-01-03 | 20          |
| 4  | 2015-01-04 | 30          |

**Output:**

| id |
|----|
| 2  |
| 4  |

**Explanation:**
On 2015-01-02, the temperature was higher than the previous day (25 > 10).
On 2015-01-04, the temperature was higher than the previous day (30 > 20).
