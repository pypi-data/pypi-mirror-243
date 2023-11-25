import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, Response, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

# Bootstrap Budget Imports
from .auth import login_required, user_only


# Define as a Flask blueprint: User
bp = Blueprint('accounts', __name__, url_prefix='/accounts')


@bp.route("/")
@login_required
@user_only
def index() -> str:
    return render_template('accounts.html')
