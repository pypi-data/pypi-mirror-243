import click
import datetime
import os
import secrets
import sqlite3

from bootstrap_budget import __version__
from importlib.resources import files
from typing import Any
from werkzeug.security import generate_password_hash


def get_db() -> sqlite3.Connection | None:
    """
    Gets a connection to the Bootstrap Budget database (if exists).

    :return: A SQLite connection to the Bootstrap Database. If the database does not exist, None is returned.
    """
    if os.path.exists('bootstrap_budget.db'):
        return sqlite3.connect('bootstrap_budget.db')
    else:
        return None


def get_current_date_iso() -> str:
    """
    Generates a timestamp for the current date/time and returned in an ISO 8601 format.

    :return: An ISO 8601 formatted timestamp of current.
    """
    # Capture current datetime for creation and update timestamps
    current_datetime = datetime.datetime.now()
    current_datetime_iso = current_datetime.isoformat()

    return current_datetime_iso


def create_schema() -> None:
    """
    Creates the Bootstrap Budget database schema. This is also used to reset the database schema as a DROP and REPLACE.

    :return: None
    """
    db_schema_script: str = files('bootstrap_budget').joinpath('db/sqlite/create_sqlite_schema.sql').read_text()
    db_connection: sqlite3.Connection = sqlite3.connect('bootstrap_budget.db')
    sql_cursor: sqlite3.Cursor = db_connection.cursor()

    # Iterate through each SQL statement in the file
    for schema_definition in db_schema_script.split('--'):
        response = sql_cursor.execute(schema_definition)

    db_connection.close()
    click.echo('The Bootstrap Budget schema has been created.')


def create_admin_account() -> None:
    """
    Creates the admin account on the USER table.

    :return: None
    """
    create_user_statement: str = files('bootstrap_budget').joinpath('db/sqlite/create_user.sql').read_text()
    db_connection: sqlite3.Connection = get_db()
    sql_cursor: sqlite3.Cursor = db_connection.cursor()

    EMPTY_STRING: str = ''

    admin_passwd = click.prompt(text='Enter admin password', type=str, default='admin',
                                show_default=True, hide_input=True)

    # Generate password hash and salt
    hashed_password = generate_password_hash(admin_passwd)

    try:
        response: sqlite3.Cursor = sql_cursor.execute(create_user_statement, [
            EMPTY_STRING,               # last_name
            EMPTY_STRING,               # first_name
            EMPTY_STRING,               # middle_name
            'admin',                    # username
            EMPTY_STRING,               # address_line_1
            EMPTY_STRING,               # address_line_2
            EMPTY_STRING,               # city
            EMPTY_STRING,               # state
            EMPTY_STRING,               # zipcode
            EMPTY_STRING,               # email
            EMPTY_STRING,               # phone_number
            hashed_password,            # hash
            get_current_date_iso(),     # created_dt_tm
            get_current_date_iso(),     # updated_dt_tm
            True                        # is_active
        ])

        db_connection.commit()
        db_connection.close()

        click.echo('The Bootstrap Budget admin account has been created.')
    except Exception as e:
        # TODO: Find a better solution for handling this exception
        click.echo(e)


def create_admin_config() -> None:
    """
    Creates the admin related configurations on the CONFIG table.
    Configurations created:
        - SECRET_KEY

    :return: None
    """
    create_config_statement: str = files('bootstrap_budget').joinpath('db/sqlite/create_config.sql').read_text()
    db_connection: sqlite3.Connection = get_db()
    sql_cursor: sqlite3.Cursor = db_connection.cursor()

    EMPTY_STRING: str = ''
    TYPE_AFFINITY_TEXT: int = 2
    ADMIN_ID: int = 1

    # Generate SECRET_KEY for Flask config
    secret_key = secrets.token_urlsafe(32)
    secret_key_description = ('A secret key that will be used for securely signing the session cookie and can be used '
                              'for any other security related needs by extensions or your application. '
                              'It should be a long random bytes or str.')

    try:
        response: sqlite3.Cursor = sql_cursor.execute(create_config_statement, [
            'SECRET_KEY',               # name
            secret_key_description,     # description
            secret_key,                 # config_value
            TYPE_AFFINITY_TEXT,         # config_value_type
            ADMIN_ID,                   # user_id
            get_current_date_iso(),     # created_dt_tm
            get_current_date_iso(),     # updated_dt_tm
            True                        # is_active
        ])

        db_connection.commit()
        db_connection.close()

        click.echo('The Bootstrap Budget SECRET_KEY has been configured.')
    except Exception as e:
        # TODO: Find a better solution for handling this exception
        click.echo(e)


def reset_admin_password() -> None:
    """
    Resets the admin account password.

    :return: None
    """
    update_admin_statement: str = 'UPDATE USERS SET hash = ?, updated_dt_tm = ? WHERE username = "admin"'
    db_connection: sqlite3.Connection = get_db()
    sql_cursor: sqlite3.Cursor = db_connection.cursor()

    admin_passwd = click.prompt(text='Enter admin password', type=str, default='admin',
                                show_default=True, hide_input=True)

    # Generate password hash and salt
    hashed_password = generate_password_hash(admin_passwd)

    try:
        response: sqlite3.Cursor = sql_cursor.execute(update_admin_statement, [
            hashed_password,            # hash
            get_current_date_iso()      # updated_dt_tm
        ])

        db_connection.commit()
        db_connection.close()

        click.echo('The Bootstrap Budget admin password has been reset.')
    except Exception as e:
        # TODO: Find a better solution for handling this exception
        click.echo(e)


def create_basic_user() -> int:
    """
    Creates a basic user (meets required fields) for the purposes of testing.

    :return: The user_id of the newly inserted user.
    """
    create_user_statement: str = files('bootstrap_budget').joinpath('db/sqlite/create_user.sql').read_text()
    db_connection: sqlite3.Connection = get_db()
    sql_cursor: sqlite3.Cursor = db_connection.cursor()

    EMPTY_STRING: str = ''
    username: str | None = None

    while username is None:
        username = click.prompt(text='Enter new username', type=str, show_default=True)

        user_id: int = sql_cursor.execute('SELECT id FROM USERS WHERE username = ?',
                                          [username]).fetchone()

        if user_id is not None:
            click.echo(f'The username "{username}" has already been taken. Please use a different username.')
            username = None
            continue

    user_password: str = click.prompt(text=f'Enter password for {username}', type=str, default=f'{username}',
                                      show_default=True, hide_input=True)

    # Generate password hash and salt
    hashed_password: str = generate_password_hash(user_password)

    try:
        response: sqlite3.Cursor = sql_cursor.execute(create_user_statement, [
            EMPTY_STRING,               # last_name
            EMPTY_STRING,               # first_name
            EMPTY_STRING,               # middle_name
            username,                   # username
            EMPTY_STRING,               # address_line_1
            EMPTY_STRING,               # address_line_2
            EMPTY_STRING,               # city
            EMPTY_STRING,               # state
            EMPTY_STRING,               # zipcode
            EMPTY_STRING,               # email
            EMPTY_STRING,               # phone_number
            hashed_password,            # hash
            get_current_date_iso(),     # created_dt_tm
            get_current_date_iso(),     # updated_dt_tm
            True                        # is_active
        ])

        # Retrieve the key generated from the insert
        new_user_id: int = sql_cursor.lastrowid

        db_connection.commit()
        db_connection.close()

        click.echo(f'The user "{username}" has been created.')

        return new_user_id
    except Exception as e:
        # TODO: Find a better solution for handling this exception
        click.echo(e)


def create_sample_data(user_id: int) -> None:
    """
    Creates a basic user (meets required fields) for the purposes of testing.

    :return: The user_id of the newly inserted user.
    """
    # Gather sample data
    budget_csv: str = files('bootstrap_budget').joinpath('db/sample_data/budget.csv').read_text()
    budget_items_csv: str = files('bootstrap_budget').joinpath('db/sample_data/budget_items.csv').read_text()
    accounts_csv: str = files('bootstrap_budget').joinpath('db/sample_data/accounts.csv').read_text()
    transactions_csv: str = files('bootstrap_budget').joinpath('db/sample_data/transactions.csv').read_text()

    # Gather insert statements
    create_budget_statement: str = files('bootstrap_budget').joinpath('db/sqlite/create_budget.sql').read_text()
    create_budget_items_statement: str = files('bootstrap_budget').joinpath('db/sqlite/create_budget_items.sql').read_text()
    create_accounts_statement: str = files('bootstrap_budget').joinpath('db/sqlite/create_accounts.sql').read_text()
    create_transactions_statement: str = files('bootstrap_budget').joinpath('db/sqlite/create_transactions.sql').read_text()

    # Define DB connection
    db_connection: sqlite3.Connection = get_db()
    sql_cursor: sqlite3.Cursor = db_connection.cursor()

    # Read and insert budget record(s)
    budget_data: list[Any] = []
    budget_records: list[Any] = budget_csv.split('\n')

    for budget_record in enumerate(budget_records):
        if budget_record[0] > 0:
            record: list = budget_record[1].split(',')
            record[2] = int(record[2])  # budget_year (conversion to int from str)
            record.append(user_id)
            record.append(get_current_date_iso())  # created_dt_tm
            record.append(get_current_date_iso())  # updated_dt_tm
            record.append(True)  # is_active
            budget_data.append(record)

    try:
        response: sqlite3.Cursor = sql_cursor.executemany(create_budget_statement, budget_data)

        db_connection.commit()

        click.echo(f'Sample BUDGET data has been inserted.')
    except Exception as e:
        # TODO: Find a better solution for handling this exception
        click.echo(e)

    # Read and insert budget item record(s)
    budget_items_data: list[Any] = []
    budget_items_records: list[Any] = budget_items_csv.split('\n')

    for budget_item_record in enumerate(budget_items_records):
        if budget_item_record[0] > 0:
            record: list = budget_item_record[1].split(',')
            record[2] = float(record[2])  # budget_amount (conversion to float from str)
            record[3] = int(record[3])  # sequence (conversion to int from str)
            record.append(user_id)
            record.append(get_current_date_iso())  # created_dt_tm
            record.append(get_current_date_iso())  # updated_dt_tm
            record.append(True)  # is_active
            budget_items_data.append(record)

    try:
        response: sqlite3.Cursor = sql_cursor.executemany(create_budget_items_statement, budget_items_data)

        db_connection.commit()

        click.echo(f'Sample BUDGET_ITEMS data has been inserted.')
    except Exception as e:
        # TODO: Find a better solution for handling this exception
        click.echo(e)

    # Read and insert account record(s)
    account_data: list[Any] = []
    account_records: list[Any] = accounts_csv.split('\n')

    for account_record in enumerate(account_records):
        if account_record[0] > 0:
            record = account_record[1].split(',')
            record[4] = float(record[4])  # opening_amount (conversion to float from str)
            record.append(user_id)
            record.append(get_current_date_iso())  # created_dt_tm
            record.append(get_current_date_iso())  # updated_dt_tm
            record.append(True)  # is_active
            account_data.append(record)

    try:
        response: sqlite3.Cursor = sql_cursor.executemany(create_accounts_statement, account_data)

        db_connection.commit()

        click.echo(f'Sample ACCOUNTS data has been inserted.')
    except Exception as e:
        # TODO: Find a better solution for handling this exception
        click.echo(e)

    # Retrieve BUDGET_ITEM records as a lookup dictionary
    budget_items_lookup: dict = {}

    try:
        response: sqlite3.Cursor = sql_cursor.execute('SELECT id, name FROM BUDGET_ITEMS WHERE user_id = ?',
                                      [user_id])
        for value, key in response:
            budget_items_lookup[key] = value
    except Exception as e:
        # TODO: Find a better solution for handling this exception
        click.echo(e)

    # Retrieve ACCOUNTS records as a lookup dictionary
    accounts_lookup: dict = {}

    try:
        response: sqlite3.Cursor = sql_cursor.execute('SELECT id, name FROM ACCOUNTS WHERE user_id = ?',
                                                      [user_id])
        for value, key in response:
            accounts_lookup[key] = value
    except Exception as e:
        # TODO: Find a better solution for handling this exception
        click.echo(e)

    # Read and insert transaction record(s)
    transaction_data: list[Any] = []
    transaction_records: list[Any] = transactions_csv.split('\n')

    for transaction_record in enumerate(transaction_records):
        if transaction_record[0] > 0:
            record = transaction_record[1].split(',')
            record[1] = float(record[1])  # amount (conversion to float from str)
            record[4] = budget_items_lookup.get(record[4], None)  # budget_item_id (lookup from dict)
            record[5] = accounts_lookup.get(record[5], None)  # budget_item_id (lookup from dict)
            record.append(user_id)
            record.append(get_current_date_iso())  # created_dt_tm
            record.append(get_current_date_iso())  # updated_dt_tm
            record.append(True)  # is_active
            transaction_data.append(record)

    try:
        response: sqlite3.Cursor = sql_cursor.executemany(create_transactions_statement, transaction_data)

        db_connection.commit()

        click.echo(f'Sample TRANSACTIONS data has been inserted.')
    except Exception as e:
        # TODO: Find a better solution for handling this exception
        click.echo(e)

    db_connection.close()


@click.command()
@click.option('--version', is_flag=True, help='Returns the current version of Bootstrap Budget installed.')
@click.option('--setup', is_flag=True, help='Creates the database schema, admin user, and base config.')
@click.option('--reset-admin', is_flag=True, help='Reset admin password.')
@click.option('--reset-bootstrap', is_flag=True, help='Reset your Bootstrap-Budget install (start over).')
@click.option('--backup', is_flag=True, help='Backup all tables to CSV (password-protected zip file).')
def bootstrap(version: bool, setup: bool, reset_admin: bool, reset_bootstrap: bool, backup: bool) -> None:
    """
    The Bootstrap Budget command-line interface utility. Used for initial setup, reset, and backing up data.

    :param version: Returns the current version of Bootstrap Budget installed.
    :param setup: Creates the database schema, admin user, and base config.
    :param reset_admin: Reset admin password.
    :param reset_bootstrap: Reset your Bootstrap-Budget install (start over).
    :param backup: Backup all tables to CSV (password-protected zip file).
    :return: None
    """
    if version:
        click.echo(f'bootstrap-budget v{__version__}')
    elif setup or reset_bootstrap:
        if get_db() is not None:
            if reset_bootstrap:
                if click.confirm('Resetting Bootstrap Budget means deleting all of your data and starting over. '
                                 'Are you sure you want to do this?'):
                    create_schema()
                    create_admin_account()
                    create_admin_config()
                    click.echo('Your Boostrap Budget install has been completely reset.')
            else:
                click.echo('Bootstrap Budget has already sbeen etup. No action is needed.')
        else:
            create_schema()
            create_admin_account()
            create_admin_config()
            click.echo('Your Boostrap Budget setup is complete!')
    elif reset_admin:
        if get_db() is not None:
            if click.confirm('You are about to reset your admin account. Are you sure you want to do this?'):
                reset_admin_password()
        else:
            click.echo('The Bootstrap Budget database has not been created. Run --setup first.')
    elif backup:
        # TODO: Complete the backup feature
        click.echo('This does nothing right now, sorry :(')


@click.command('bootstrap-test')
@click.option('--create-user', is_flag=True, help='Creates a basic user for testing purposes.')
@click.option('--create-sample', is_flag=True, help='Inserts sample data set with test user.')
def bootstrap_test(create_user: bool, create_sample: bool) -> None:
    """
    The Bootstrap Budget TEST command-line interface utility. Used for setting up test users and sample data.

    :param create_user: Creates a basic user for testing purposes.
    :param create_sample: Inserts sample data set with test user.
    :return: None
    """
    if create_user:
        if get_db() is not None:
            create_basic_user()
        else:
            click.echo('The Bootstrap Budget database has not been created. Run --setup first.')
    elif create_sample:
        if get_db() is not None:
            user_id = create_basic_user()
            create_sample_data(user_id=user_id)

            click.echo('Sample data has been successfully inserted.')
        else:
            click.echo('The Bootstrap Budget database has not been created. Run --setup first.')


if __name__ == '__main__':
    pass
