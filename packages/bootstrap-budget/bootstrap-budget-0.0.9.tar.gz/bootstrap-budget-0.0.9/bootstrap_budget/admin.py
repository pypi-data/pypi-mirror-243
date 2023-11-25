import functools

from flask import (
    Blueprint, current_app, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash

# Import bootstrap-budget blueprints/modules/classes/functions
from .auth import login_required, admin_only
from .db import get_db


# Define as a Flask blueprint: Admin
bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route("/")
@login_required
@admin_only
def index():
    return render_template('admin.html')


@bp.route("/users")
@login_required
@admin_only
def users():
    return render_template('users.html')


@bp.route("/shutdown", methods=['POST'])
@login_required
@admin_only
def shutdown():
    if request.method == 'POST':
        form_password = request.form['password']

        db = get_db()

        error = None

        password_hash = db.execute('SELECT hash FROM USERS WHERE username = "admin"').fetchone()

        if check_password_hash(password_hash, form_password):
            current_app.logger.info('Admin password checks out. Trying to shutdown...')
