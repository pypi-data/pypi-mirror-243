import sqlite3

from flask import g


def get_db() -> sqlite3.Connection:
    """
    Create and/or retrieve the SQLite DB connection as a Flask global (g) property

    :return: A SQLite connection
    """
    if 'db' not in g:
       g.db = sqlite3.connect(database='bootstrap_budget.db',
                              detect_types=sqlite3.PARSE_DECLTYPES)
       g.db.row_factory = sqlite3.Row

    return g.db


def close_db() -> None:
    """
    Close the database connection.

    :return: None
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


if __name__ == '__main__':
    pass
