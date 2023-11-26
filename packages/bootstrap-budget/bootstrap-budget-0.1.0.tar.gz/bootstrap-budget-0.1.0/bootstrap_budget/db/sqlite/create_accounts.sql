/*
 * Name: create_accounts.sql
 * Purpose: Creates ACCOUNTS record(s).
 * Author: Blake Phillips (forgineer)
 */
INSERT INTO ACCOUNTS (
    name
    , description
    , account_number
    , account_route_nbr
    , opening_amount
    , user_id
    , created_dt_tm
    , updated_dt_tm
    , is_active)
VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);