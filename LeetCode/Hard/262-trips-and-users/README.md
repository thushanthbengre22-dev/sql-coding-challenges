# Trips and Users

## Problem Description

Table: `Trips`

| Column Name | Type                                       |
|-------------|--------------------------------------------|
| id          | int                                        |
| client_id   | int                                        |
| driver_id   | int                                        |
| city_id     | int                                        |
| status      | enum('completed','cancelled_by_driver','cancelled_by_client') |
| request_at  | varchar                                    |

`id` is the primary key for this table.
`client_id` and `driver_id` are foreign keys referencing `Users.users_id`.

Table: `Users`

| Column Name | Type               |
|-------------|--------------------|
| users_id    | int                |
| banned      | enum('Yes', 'No')  |
| role        | enum('client','driver','partner') |

`users_id` is the primary key for this table.

The **cancellation rate** is computed by dividing the number of cancelled (by client or driver) requests with unbanned users by the total number of requests with unbanned users on that day.

Write a solution to find the **cancellation rate** of requests with unbanned users (**both client and driver must be unbanned**) each day between `2013-10-01` and `2013-10-03`. Round the cancellation rate to two decimal points.

Return the result table ordered by `Day`.

## Example 1

**Input:**

`Trips` table:

| id | client_id | driver_id | city_id | status              | request_at |
|----|-----------|-----------|---------|---------------------|------------|
| 1  | 1         | 10        | 1       | completed           | 2013-10-01 |
| 2  | 2         | 11        | 1       | cancelled_by_driver | 2013-10-01 |
| 3  | 3         | 12        | 6       | completed           | 2013-10-01 |
| 4  | 4         | 13        | 6       | cancelled_by_client | 2013-10-01 |
| 5  | 1         | 10        | 1       | completed           | 2013-10-02 |
| 6  | 2         | 11        | 6       | completed           | 2013-10-02 |
| 7  | 3         | 12        | 6       | completed           | 2013-10-02 |
| 8  | 2         | 12        | 12      | completed           | 2013-10-03 |
| 9  | 3         | 10        | 12      | completed           | 2013-10-03 |
| 10 | 4         | 13        | 12      | cancelled_by_driver | 2013-10-03 |

`Users` table:

| users_id | banned | role   |
|----------|--------|--------|
| 1        | No     | client |
| 2        | Yes    | client |
| 3        | No     | client |
| 4        | No     | client |
| 10       | No     | driver |
| 11       | No     | driver |
| 12       | No     | driver |
| 13       | No     | driver |

**Output:**

| Day        | Cancellation Rate |
|------------|-------------------|
| 2013-10-01 | 0.33              |
| 2013-10-02 | 0.00              |
| 2013-10-03 | 0.50              |

**Explanation:**
On 2013-10-01: trips 2 and 6 involve banned user 2 and are excluded. Of the remaining 3 trips, 1 was cancelled → rate = 0.33.
On 2013-10-02: trips involving banned user 2 are excluded. Of the remaining 2 trips, 0 cancelled → rate = 0.00.
On 2013-10-03: trips involving banned user 2 are excluded. Of the remaining 2 trips, 1 cancelled → rate = 0.50.
