# Delete Duplicate Emails

## Problem Description

Table: `Person`

| Column Name | Type    |
|-------------|---------|
| id          | int     |
| email       | varchar |

`id` is the primary key for this table.
Each row contains an email address. Emails will not contain uppercase letters.

Write a solution to delete all duplicate emails, keeping only one unique email with the **smallest** `id`.

Note that you are supposed to write a `DELETE` statement, not a `SELECT` one.

## Example 1

**Input:**

`Person` table:

| id | email            |
|----|------------------|
| 1  | john@example.com |
| 2  | bob@example.com  |
| 3  | john@example.com |

**Output:**

| id | email            |
|----|------------------|
| 1  | john@example.com |
| 2  | bob@example.com  |

**Explanation:**
`john@example.com` appeared twice. The row with the smallest id (1) is kept and the duplicate (id=3) is deleted.