/*
 * Name: create_sqlite_schema.sql
 * Purpose: Creates the Bootstrap Budget table schema for SQLite.
 * Author: Blake Phillips (forgineer)
 */
DROP TABLE IF EXISTS CONFIG;
--
DROP TABLE IF EXISTS TRANSACTIONS;
--
DROP TABLE IF EXISTS USER_BUDGET;
--
DROP TABLE IF EXISTS ACCOUNTS;
--
DROP TABLE IF EXISTS BUDGET_ITEMS;
--
DROP TABLE IF EXISTS BUDGET;
--
DROP TABLE IF EXISTS USERS;
--
CREATE TABLE USERS (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	last_name TEXT,
	first_name TEXT,
	middle_name TEXT,
	username TEXT UNIQUE NOT NULL,
	address_line_1 TEXT,
	address_line_2 TEXT,
	city TEXT,
	state TEXT,
	zipcode TEXT,
	email TEXT,
	phone_number TEXT,
	hash TEXT NOT NULL,
	created_dt_tm TEXT NOT NULL,
	updated_dt_tm TEXT NOT NULL,
	is_active INTEGER DEFAULT 1 NOT NULL
);
--
CREATE TABLE CONFIG (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL,
	description TEXT,
	config_value TEXT,
	config_value_type INTEGER DEFAULT 0 NOT NULL,
	user_id INTEGER NOT NULL,
	created_dt_tm TEXT NOT NULL,
	updated_dt_tm TEXT NOT NULL,
	is_active INTEGER DEFAULT 1 NOT NULL,
	FOREIGN KEY (user_id) REFERENCES USERS (id),
	UNIQUE(name, user_id)
);
--
CREATE TABLE BUDGET (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL,
	description TEXT,
	budget_year INTEGER NOT NULL,
	user_id INTEGER NOT NULL,
	created_dt_tm TEXT NOT NULL,
	updated_dt_tm TEXT NOT NULL,
	is_active INTEGER DEFAULT 1 NOT NULL,
	FOREIGN KEY (user_id) REFERENCES USERS (id),
	UNIQUE(name, user_id)
);
--
CREATE TABLE USER_BUDGET (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	user_id INTEGER NOT NULL,
	budget_id INTEGER NOT NULL,
	permissions INTEGER NOT NULL,
	created_dt_tm TEXT NOT NULL,
	updated_dt_tm TEXT NOT NULL,
	is_active INTEGER DEFAULT 1 NOT NULL,
	FOREIGN KEY (budget_id) REFERENCES BUDGET (id),
	FOREIGN KEY (user_id) REFERENCES USERS (id)
);
--
CREATE TABLE BUDGET_ITEMS (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL,
	description TEXT,
	budget_amount REAL DEFAULT 0.0 NOT NULL,
	sequence INTEGER DEFAULT 99 NOT NULL,
	user_id INTEGER NOT NULL,
	created_dt_tm TEXT NOT NULL,
	updated_dt_tm TEXT NOT NULL,
	is_active INTEGER DEFAULT 1 NOT NULL,
	FOREIGN KEY (user_id) REFERENCES USERS (id),
	UNIQUE(name, user_id)
);
--
CREATE TABLE ACCOUNTS (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL,
	description TEXT,
	account_number TEXT,
	account_route_nbr TEXT,
	opening_amount REAL DEFAULT 0.0 NOT NULL,
	user_id INTEGER NOT NULL,
	created_dt_tm TEXT NOT NULL,
	updated_dt_tm TEXT NOT NULL,
	is_active INTEGER DEFAULT 1 NOT NULL,
	FOREIGN KEY (user_id) REFERENCES USERS (id),
	UNIQUE(name, user_id)

);
--
CREATE TABLE TRANSACTIONS (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	description TEXT,
	amount REAL DEFAULT 0.0 NOT NULL,
	transaction_dt_tm TEXT NOT NULL,
	transaction_year INTEGER GENERATED ALWAYS AS (STRFTIME('%Y', transaction_dt_tm)) VIRTUAL,
	transaction_month INTEGER GENERATED ALWAYS AS (STRFTIME('%m', transaction_dt_tm)) VIRTUAL,
	transaction_day INTEGER GENERATED ALWAYS AS (STRFTIME('%d', transaction_dt_tm)) VIRTUAL,
	note TEXT,
	budget_item_id INTEGER DEFAULT 0 NOT NULL,
	account_id INTEGER DEFAULT 0 NOT NULL,
	user_id INTEGER NOT NULL,
	created_dt_tm TEXT NOT NULL,
	updated_dt_tm TEXT NOT NULL,
	is_active INTEGER DEFAULT 1 NOT NULL,
	FOREIGN KEY (account_id) REFERENCES ACCOUNTS (id),
	FOREIGN KEY (budget_item_id) REFERENCES BUDGET_ITEMS (id),
	FOREIGN KEY (user_id) REFERENCES USERS (id)
);
