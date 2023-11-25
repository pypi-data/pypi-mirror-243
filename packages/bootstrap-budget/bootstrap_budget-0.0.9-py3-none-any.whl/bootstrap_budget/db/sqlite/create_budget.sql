/*
 * Name: create_budget.sql
 * Purpose: Creates BUDGET record(s).
 * Author: Blake Phillips (forgineer)
 */
INSERT INTO BUDGET (
    name
    , description
    , budget_year
    , user_id
    , created_dt_tm
    , updated_dt_tm
    , is_active)
VALUES(?, ?, ?, ?, ?, ?, ?);