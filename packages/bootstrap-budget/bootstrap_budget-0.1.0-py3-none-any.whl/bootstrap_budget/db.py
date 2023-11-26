import os
import sqlite3

from flask import current_app, g


def get_db() -> sqlite3.Connection | None:
    """
    Create and/or retrieve the SQLite DB connection as a Flask global (g) property

    :return: A SQLite connection or None if the Db is not setup yet (raise error)
    """
    if 'db' not in g:
        if os.path.exists('bootstrap_budget.db'):
            g.db = sqlite3.connect(database='bootstrap_budget.db',
                                   detect_types=sqlite3.PARSE_DECLTYPES)
            g.db.row_factory = sqlite3.Row
        else:
            return None
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
