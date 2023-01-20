from cs50 import SQL
from wtforms import Form, StringField, PasswordField, EmailField, ValidationError
from wtforms.validators import InputRequired, Length, Email, Regexp
from wtforms.widgets import TextArea
from flask import Markup, url_for
from functools import wraps
from flask import request, redirect, session, render_template

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///invoicer.db")

# ---------------------------------------------------------------------------- #
#                         LOGIN/EMAIL AUTH + LOGIN REDIRECT                    #
# ---------------------------------------------------------------------------- #

def login_and_verification_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("id"):
            return redirect(url_for("login"))
        if not session.get("verified"):
            return render_template("verify.html")
        return f(*args, **kwargs)
    return decorated_function


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("id"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


def redirect_if_logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("id"):
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# ---------------------------------------------------------------------------- #
#                                    WTFORMS                                   #
# ---------------------------------------------------------------------------- #

class RegistrationForm(Form):
    details_label = Markup('Company Details <br> <span class="small">(e.g. Address, Contact No.)</span>')

    username = StringField('Username', validators=[InputRequired("Username is required"),
                                        Regexp(r'^[\w_]+$', message="Username can only contain alphanumerical characters or underscore"),
                                        Length(min=6, max=18, message="Minimum and maximum length of username is 6 and 18")])
    password = PasswordField('Password', validators=[InputRequired("Password is required"),
                                        Length(min=8, message="Minimum length of password is 8")])
    email = EmailField('Email', validators=[InputRequired("Email is required"),
                                 Email("Invalid email", check_deliverability=True)])
    name = StringField('Name', validators=[InputRequired("Name is required")])
    details = StringField(details_label, widget=TextArea())

class LoginForm(Form):
    username = StringField('Username', validators=[InputRequired("Username is required")])
    password = PasswordField('Password', validators=[InputRequired("Password is required")])

class ResetForm(Form):
    old = PasswordField('Old Password: ', validators=[InputRequired("Password is required")])
    new = PasswordField('New Password: ', validators=[InputRequired("Password is required"),
                                    Length(min=8, message="Minimum length of password is 8")])
    confirm = PasswordField('Confirm New Password: ', validators=[InputRequired("Password is required")])

# ---------------------------------------------------------------------------- #
#                            OTHER FUNCTIONS                                   #
# ---------------------------------------------------------------------------- #

# Read and execute two SQL Scripts
# 1. Insert duplicated main data
# 2. Duplicate "table items" into new ID
def copy_sqlscripts(main, items, id):
    copy = open(f'sqlcommands/{main}.sql', 'r')
    copyitems = open(f'sqlcommands/{items}.sql', 'r')
    new_id = db.execute(copy.read(), id)
    db.execute(copyitems.read(), new_id, id)
    copy.close()
    copyitems.close()
    return new_id