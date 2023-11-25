import functools

from flask import (
    abort, Blueprint, flash, g, redirect, render_template, request, Response, session, url_for
)
from werkzeug.security import check_password_hash

# Import bootstrap-budget blueprints/modules/classes/functions
from .db import get_db


# Define as a Flask blueprint: Auth
bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


def admin_only(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session['username'] == 'admin':
            return view(**kwargs)
        else:
            return redirect(url_for('dashboard.index'))
            #return abort(403)  # TODO: Go nowhere, or warn user that they do not have access.

    return wrapped_view


def user_only(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session['username'] != 'admin':
            return view(**kwargs)
        else:
            return redirect(url_for('admin.index'))
            #return abort(403)  # TODO: Go nowhere, or warn user that they do not have access.

    return wrapped_view


@bp.before_app_request
def load_logged_in_user() -> None:
    """
    If a user id is stored in the session, load the user object from the database into `g.user`.

    :return: None
    """
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM USERS WHERE id = ?",
                             (user_id,)).fetchone()
        )


@bp.route('/login', methods=['GET', 'POST'])
def login() -> Response | str:
    # TODO: Prevent users from being able to reach this after they have already logged in.
    if request.method == 'POST':
        form_username = request.form['username']
        form_password = request.form['password']

        db = get_db()

        error = None

        user_id, password_hash = db.execute('SELECT id, hash FROM USERS WHERE username = ?',
                                            [form_username]).fetchone()

        if password_hash is None:
            error = 'Incorrect username.'
        elif not check_password_hash(password_hash, form_password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user_id
            session['username'] = form_username

            if form_username == 'admin':
                return redirect(url_for('admin.index'))
            else:
                return redirect(url_for('dashboard.index'))

        flash(error)

    return render_template('login.html')


@bp.route('/logout')
def logout() -> Response:
    session.clear()
    return redirect(url_for('dashboard.index'))
