/*
 * Name: create_budget_items.sql
 * Purpose: Creates BUDGET_ITEMS record(s).
 * Author: Blake Phillips (forgineer)
 */
INSERT INTO BUDGET_ITEMS (
    name
    , description
    , budget_amount
    , "sequence"
    , user_id
    , created_dt_tm
    , updated_dt_tm
    , is_active)
VALUES(?, ?, ?, ?, ?, ?, ?, ?);