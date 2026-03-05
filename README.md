# SQL Coding Challenges

This repository contains my solutions to various SQL coding challenges, primarily from LeetCode.

## Problems

| Platform | Difficulty | ID | Title | Problem | Solution | Tests |
|---|---|---|---|---|---|---|
| LeetCode | Easy | 175 | Combine Two Tables | [README](LeetCode/Easy/175-combine-two-tables/README.md) | [SQL](LeetCode/Easy/175-combine-two-tables/solution.sql) | [test](LeetCode/Easy/175-combine-two-tables/test_solution.py) |
| LeetCode | Easy | 181 | Employees Earning More Than Their Managers | [README](LeetCode/Easy/181-employee-earning-more-than-manager/README.md) | [SQL](LeetCode/Easy/181-employee-earning-more-than-manager/solution.sql) | [test](LeetCode/Easy/181-employee-earning-more-than-manager/test_solution.py) |
| LeetCode | Easy | 182 | Duplicate Emails | [README](LeetCode/Easy/182-duplicate-emails/README.md) | [SQL](LeetCode/Easy/182-duplicate-emails/solution.sql) | [test](LeetCode/Easy/182-duplicate-emails/test_solution.py) |
| LeetCode | Medium | 176 | Second Highest Salary | [README](LeetCode/Medium/176-second-highest-salary/README.md) | [SQL](LeetCode/Medium/176-second-highest-salary/solution.sql) | [test](LeetCode/Medium/176-second-highest-salary/test_solution.py) |
| LeetCode | Medium | 177 | Nth Highest Salary | [README](LeetCode/Medium/177-nth-highest-salary/README.md) | [SQL](LeetCode/Medium/177-nth-highest-salary/solution.sql) | [test](LeetCode/Medium/177-nth-highest-salary/test_solution.py) |
| LeetCode | Medium | 178 | Rank Scores | [README](LeetCode/Medium/178-rank-scores/README.md) | [SQL](LeetCode/Medium/178-rank-scores/solution.sql) | [test](LeetCode/Medium/178-rank-scores/test_solution.py) |
| LeetCode | Easy | 183 | Customers Who Never Order | [README](LeetCode/Easy/183-customer-who-never-orders/README.md) | [SQL](LeetCode/Easy/183-customer-who-never-orders/solution.sql) | [test](LeetCode/Easy/183-customer-who-never-orders/test_solution.py) |
| LeetCode | Medium | 180 | Consecutive Numbers | [README](LeetCode/Medium/180-consecutive-numbers/README.md) | [SQL](LeetCode/Medium/180-consecutive-numbers/solution.sql) | [test](LeetCode/Medium/180-consecutive-numbers/test_solution.py) |
| LeetCode | Medium | 184 | Department Highest Salary | [README](LeetCode/Medium/184-department-highest-salary/README.md) | [SQL](LeetCode/Medium/184-department-highest-salary/solution.sql) | [test](LeetCode/Medium/184-department-highest-salary/test_solution.py) |
| LeetCode | Hard | 185 | Department Top Three Salaries | [README](LeetCode/Hard/185-dept-top-three-salary/README.md) | [SQL](LeetCode/Hard/185-dept-top-three-salary/solution.sql) | [test](LeetCode/Hard/185-dept-top-three-salary/test_solution.py) |
| LeetCode | Easy | 196 | Delete Duplicate Emails | [README](LeetCode/Easy/196-delete-duplicate-emails/README.md) | [SQL](LeetCode/Easy/196-delete-duplicate-emails/solution.sql) | [test](LeetCode/Easy/196-delete-duplicate-emails/test_solution.py) |

## Problem Format

Each problem directory contains:
- `README.md`: Problem description and examples.
- `solution.sql`: SQL solution.
- `test_solution.py`: pytest tests that validate the solution against an in-memory SQLite database.

## Running Tests

**Setup** (first time only):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Run all tests:**

```bash
pytest
```

**Run tests for a specific problem:**

```bash
pytest LeetCode/Easy/182-duplicate-emails/
```

**Run with verbose output:**

```bash
pytest -v
```

Tests use an in-memory SQLite database, so no external database setup is required.

## Goals

- Practice and improve SQL skills.
- Document solutions for future reference.
- Share knowledge with the community.