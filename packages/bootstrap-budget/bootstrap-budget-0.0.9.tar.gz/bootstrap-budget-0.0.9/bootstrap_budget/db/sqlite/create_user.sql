/*
 * Name: create_users.sql
 * Purpose: Creates USERS record(s).
 * Author: Blake Phillips (forgineer)
 */
INSERT INTO USERS (
    last_name
    , first_name
    , middle_name
    , username
    , address_line_1
    , address_line_2
    , city
    , state
    , zipcode
    , email
    , phone_number
    , hash
    , created_dt_tm
    , updated_dt_tm
    , is_active)
VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);