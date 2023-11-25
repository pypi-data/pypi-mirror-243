/*
 * Name: create_transactions.sql
 * Purpose: Creates TRANSACTIONS record(s).
 * Author: Blake Phillips (forgineer)
 */
INSERT INTO TRANSACTIONS (
    description
    , amount
    , transaction_dt_tm
    , note
    , budget_item_id
    , account_id
    , user_id
    , created_dt_tm
    , updated_dt_tm
    , is_active)
VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);