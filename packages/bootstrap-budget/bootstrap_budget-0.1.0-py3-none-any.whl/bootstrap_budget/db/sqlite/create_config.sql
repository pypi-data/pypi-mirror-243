/*
 * Name: create_config.sql
 * Purpose: Creates CONFIG record.
 * Author: Blake Phillips (forgineer)
 */
INSERT INTO CONFIG (
    name
    , description
    , config_value
    , config_value_type
    , user_id
    , created_dt_tm
    , updated_dt_tm
    , is_active)
VALUES(?, ?, ?, ?, ?, ?, ?, ?);