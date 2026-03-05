# Customers Who Never Order

## Problem Description

Table: `Customers`

| Column Name | Type    |
|-------------|---------|
| id          | int     |
| name        | varchar |

`id` is the primary key for this table.
Each row contains the ID and name of a customer.

Table: `Orders`

| Column Name | Type |
|-------------|------|
| id          | int  |
| customerId  | int  |

`id` is the primary key for this table.
`customerId` is a foreign key referencing `Customers.id`.
Each row contains the ID of an order and the ID of the customer who placed it.

Write a solution to find all customers who never placed an order.

Return the result table in any order.

## Example 1

**Input:**

`Customers` table:

| id | name  |
|----|-------|
| 1  | Joe   |
| 2  | Henry |
| 3  | Sam   |
| 4  | Max   |

`Orders` table:

| id | customerId |
|----|------------|
| 1  | 3          |
| 2  | 1          |

**Output:**

| Customers |
|-----------|
| Henry     |
| Max       |

**Explanation:**
Henry (id=2) and Max (id=4) have no entries in the Orders table.