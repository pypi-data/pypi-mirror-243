import datetime
import functools
import sqlite3

from dataclasses import dataclass
from flask import (
    Blueprint, flash, g, redirect, render_template, request, Response, session, url_for
)
from importlib.resources import files
from werkzeug.security import check_password_hash, generate_password_hash

# Bootstrap Budget Imports
from .auth import login_required, user_only


# Define as a Flask blueprint: User
bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route("/")
@login_required
@user_only
def index() -> str:
    return render_template('dashboard.html')


class Users:
    # USERS table fields
    last_name: str
    first_name: str
    middle_name: str
    username: str
    address_line_1: str
    address_line_2: str
    city: str
    state: str
    zipcode: str
    email: str
    phone_number: str
    hash: str
    salt: str
    is_admin: bool
    created_dt_tm: datetime
    updated_dt_tm: datetime
    is_active: bool

    # Constants
    EMPTY_STRING: str = ''

    def __init__(self, username: str, **fields) -> None:
        self.last_name = fields.get('last_name', self.EMPTY_STRING)
        self.first_name = fields.get('first_name', self.EMPTY_STRING)
        self.middle_name = fields.get('middle_name', self.EMPTY_STRING)
        self.username = username
        self.address_line_1 = fields.get('address_line_1', self.EMPTY_STRING)
        self.address_line_2 = fields.get('address_line_2', self.EMPTY_STRING)
        self.city = fields.get('city', self.EMPTY_STRING)
        self.state = fields.get('state', self.EMPTY_STRING)
        self.zipcode = fields.get('zipcode', self.EMPTY_STRING)
        self.email = fields.get('email', self.EMPTY_STRING)
        self.phone_number = fields.get('phone_number', self.EMPTY_STRING)
        self.is_admin = fields.get('is_admin', False)
        self.is_active = fields.get('is_active', True)

    def create(self, user_password: str) -> None:
        insert_user: str = files('bootstrap_budget').joinpath('db/sqlite/create_user.sql').read_text()
        db_connection: sqlite3.Connection = sqlite3.connect(f'bootstrap_budget.db')
        sql_cursor: sqlite3.Cursor = db_connection.cursor()

        # Generate password hash and salt
        hashed_password = generate_password_hash(user_password)

        # Capture current datetime for creation and update timestamps
        current_datetime = datetime.datetime.now()
        current_datetime_iso = current_datetime.isoformat()

        try:
            response = sql_cursor.execute(insert_user, [
                self.last_name,
                self.first_name,
                self.middle_name,
                self.username,
                self.address_line_1,
                self.address_line_2,
                self.city,
                self.state,
                self.zipcode,
                self.email,
                self.phone_number,
                hashed_password,  # hash
                self.is_admin,
                current_datetime_iso,  # created_dt_tm
                current_datetime_iso,  # updated_dt_tm
                self.is_active
            ])

            db_connection.commit()
        except Exception as e:
            print(e)

        db_connection.close()


def get_users() -> list[Users]:
    pass
