import os
from random import randint
import sqlite3
from cs50 import SQL
from wsgiref import validate
from flask import Flask, redirect, render_template, request, session, flash, url_for
from helpers import RegistrationForm, LoginForm, ResetForm, login_required, login_and_verification_required, redirect_if_logged_in, copy_sqlscripts
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from datetime import datetime, timedelta

# Create Flask instance
app = Flask(__name__)

# Create a Mail instance
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get("CS50FP_MAIL_USERNAME")
app.config['MAIL_PASSWORD'] =  os.environ.get("CS50FP_MAIL_PASSWORD")
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# Configuration
app.config['SECRET_KEY'] = os.environ.get("CS50FP_SECRET_KEY")
app.config['PERMANENT_SESSION_LIFETIME'] = 36000

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///invoicer.db")

# Constant variables
TEN_MINUTES = timedelta(minutes=10)

# ---------------------------------------------------------------------------- #
#                                    ROUTES                                    #
# ---------------------------------------------------------------------------- #

@app.route("/register", methods=['GET', 'POST'])
@redirect_if_logged_in
def register():
    reg_form = RegistrationForm(request.form, prefix="reg_")

    # Validate user input
    if request.method == 'POST':

        # Backend form validation
        if not reg_form.validate():
            flash("Please ensure valid input", "error")
            return render_template("register.html", reg_form=reg_form)

        # Check for duplicate username or email in the user table
        check_username = db.execute("SELECT * FROM user WHERE username = ?", reg_form.username.data)
        check_email = db.execute("SELECT * FROM user WHERE email = ?", reg_form.email.data)
        if check_username or check_email:
            if check_username:
                reg_form.username.errors.append("Username not available, try something else!")
            if check_email:
                reg_form.email.errors.append("This email has been registered before.")
            return render_template("register.html", reg_form=reg_form)

        # Register user into database
        db.execute("INSERT INTO user (username, password, email, name, details) VALUES (?, ?, ?, ?, ?)",
                   reg_form.username.data, generate_password_hash(reg_form.password.data),
                   reg_form.email.data, reg_form.name.data, reg_form.details.data)

        # Get ID of user to log them in
        userdata = db.execute("SELECT * FROM user WHERE email = ?", reg_form.email.data)
        session['id'] = userdata[0]['id']
        return redirect(url_for('verify'), code=307)

    return render_template("register.html", reg_form=reg_form)


@app.route("/login", methods=['GET', 'POST'])
@redirect_if_logged_in
def login():
    log_form = LoginForm(request.form, prefix="log_")

    # Validate user input
    if request.method == 'POST' and log_form.validate():
        userdata = db.execute("SELECT * FROM user WHERE username = ?", log_form.username.data)

        if len(userdata) != 1 or not check_password_hash(userdata[0]['password'], log_form.password.data):
            flash("Invalid username or password", "error")
            return render_template("login.html", log_form=log_form)

        # Log user's session and check for user's email verification
        session['id'] = userdata[0]['id']
        flash("Login Successful!", "info")
        if not userdata[0]['emailverification']:
            return render_template("verify.html")

        session['verified'] = True
        return redirect(url_for('index'))

    return render_template("login.html", log_form=log_form)


@app.route("/verify", methods=['GET', 'POST'])
@login_required
def verify():
    # Redirect users if not logged in / already verified
    if session.get("verified"):
        return redirect(url_for('index'))

    if request.method == 'POST':
        user_email = db.execute("SELECT email FROM user WHERE id = ?", session['id'])[0]['email']

        if request.form.get('submit'):
            # Check OTP validity
            input_code = request.form.get('code')
            user_code = db.execute("SELECT * FROM otp WHERE user_id = ?", session['id'])[0]
            time_diff = datetime.now() - datetime.strptime(user_code['timestamp'], "%Y-%m-%d %H:%M:%S")

            if str(user_code['otp']) != input_code:
                print(user_code['otp'])
                flash("Invalid input, try again.", "error")
                return render_template("verify.html")

            if time_diff > TEN_MINUTES:
                flash("OTP has expired, please request for a new one.", "error")
                return render_template("verify.html")

            # Verify user's email in database and set session to verified
            db.execute("UPDATE user SET emailverification = True WHERE email = ?", user_email)
            if session['id']:
                session['verified'] = True
            flash("Your email has been successfully verified!", "info")
            return redirect(url_for('index'))

        # Create a temporary number as OTP
        code = randint(100000, 999999)
        db.execute("INSERT OR REPLACE INTO otp(user_id, otp, timestamp) VALUES(?, ?, ?)", session['id'], code, datetime.now())

        # Send an email with the verification OTP
        msg = Message(subject="Verify your email on Invoicer!",
                      sender=('Invoicer', os.environ.get("CS50FP_MAIL_USERNAME")),
                      recipients=[user_email])
        msg.body = f"Your verification code is {code}. Please do not share this with others. It will expire in 10 minutes."
        mail.send(msg)
        sent = True
        return render_template("verify.html", sent=sent)

    return render_template("verify.html")


@app.route("/")
@login_and_verification_required
def index():
    name = db.execute("SELECT name FROM user WHERE id = ?", session['id'])[0]['name']
    quotations = db.execute("SELECT id, title, last_saved FROM quote WHERE user_id = ? ORDER BY last_saved DESC LIMIT 5", session['id'])
    invoices = db.execute("SELECT id, title, last_saved FROM invoice WHERE user_id = ? ORDER BY last_saved DESC LIMIT 5", session['id'])
    unpaid = db.execute("SELECT COUNT(status), ifnull(SUM(total_money), 0) FROM invoice WHERE user_id = ? AND status = 2", session['id'])[0]
    return render_template("index.html", name=name, quotations=quotations, invoices=invoices, unpaid=unpaid)


@app.route("/quotations/create", methods=['POST'])
@login_and_verification_required
def create_quote():
    if request.method == 'POST':
        # Create a template quotation with user info & quotation name
        quotation_name = request.form.get('quotation_name')
        userdata = db.execute("SELECT * FROM user WHERE id = ?", session['id'])[0]
        quote_id = db.execute("INSERT INTO quote (user_id, title, sender_name, sender_details) VALUES (?, ?, ?, ?)", userdata['id'], quotation_name, userdata['name'], userdata['details'])
        db.execute("INSERT INTO quote_items (quote_id, table_index, unit, rate) VALUES (?, ?, ?, ?)", quote_id, '01', '1', '0.00')

        return redirect(url_for('view_quote', quote_id=quote_id))


@app.route("/quotations", methods=['GET', 'POST'])
@login_and_verification_required
def quotations():
    if request.method == 'POST':
        quote_id = request.form.get('id')
        quote_details = db.execute("SELECT user_id FROM quote WHERE id = ?", quote_id)

        if len(quote_details) == 1 and quote_details[0]['user_id'] == session['id']:
            if request.form.get('delete'):
                db.execute("DELETE FROM quote WHERE id = ?", quote_id)
                return redirect(url_for('quotations'))

            # Edit quotation name
            if request.form.get('edit'):
                quote_name = request.form.get('name')
                db.execute("UPDATE quote SET title = ?, last_saved = ? WHERE id = ?", quote_name, datetime.now(), quote_id)

            # Duplicate quotation
            if request.form.get('copy'):
                copy_sqlscripts('copyquote', 'copyquoteitems', quote_id)

            # Convert quotation to invoice
            if request.form.get('convert'):
                copy_sqlscripts('convertquote', 'convertquoteitems', quote_id)
                return redirect(url_for('invoices'))

        else:
            flash("Error, invalid input", "error")

    quotes = db.execute("SELECT * FROM quote WHERE user_id = ? ORDER BY last_saved DESC", session['id'])
    return render_template("quotations.html", quotes=quotes)


@app.route("/quotations/<int:quote_id>", methods=['GET', 'POST'])
@login_and_verification_required
def view_quote(quote_id):
    # Validate if user is authorised to see this quote
    user_id = db.execute("SELECT user_id FROM quote WHERE id = ?", quote_id)
    if len(user_id) != 1 or user_id[0]['user_id'] != session['id']:
        return redirect(url_for('quotations'))

    if request.method == 'POST':
        # Update and submit details of quotation by user
        if request.form.get("save"):
            form = dict(request.form.items())
            db.execute("""UPDATE quote
                        SET sender_name=?, sender_details=?, recipient_details=?, project_details=?, send_date=?, ref=?, valid_till=?, total_money=?, footnote=?, last_saved=?
                        WHERE id = ?""",
                        form['sender-name'], form['sender-details'], form['recipient-details'], form['project-details'], form['send-date'], form['ref'], form['valid-till'], form['total-money'], form['footnote'], datetime.now(),
                        quote_id)

            # Update table rows for this quotation
            db.execute("DELETE FROM quote_items WHERE quote_id = ?", quote_id)
            for name in request.form:
                if 'row' in name:
                    row = request.form.getlist(name)
                    db.execute("INSERT INTO quote_items (quote_id, table_index, table_description, unit, rate, total) VALUES (?, ?, ?, ?, ?, ?)", quote_id, row[0], row[1], row[2], row[3], row[4])

        # Convert quotation to invoice
        if request.form.get("convert"):
            invoice_id = copy_sqlscripts('convertquote', 'convertquoteitems', quote_id)
            return redirect(url_for('view_invoice', invoice_id=invoice_id))

    quote_details = db.execute("SELECT * FROM quote WHERE id = ?", quote_id)[0]
    quote_items = db.execute("SELECT * FROM quote_items WHERE quote_id = ? ORDER BY table_index", quote_id)
    return render_template("view_quote.html", details=quote_details, items=quote_items)


@app.route("/invoices", methods=['GET', 'POST'])
@login_and_verification_required
def invoices():
    if request.method == 'POST':
        invoice_id = request.form.get('id')
        invoice_details = db.execute("SELECT user_id FROM invoice WHERE id = ?", invoice_id)

        if len(invoice_details) == 1 and invoice_details[0]['user_id'] == session['id']:
            if request.form.get('delete'):
                db.execute("DELETE FROM invoice WHERE id = ?", invoice_id)
                return redirect(url_for('invoices'))

            # Edit invoice name
            if request.form.get('edit'):
                invoice_name = request.form.get('name')
                db.execute("UPDATE invoice SET title = ?, last_saved = ? WHERE id = ?", invoice_name, datetime.now(), invoice_id)

            # Duplicate invoice
            if request.form.get('copy'):
                copy_sqlscripts('copyinvoice', 'copyinvoiceitems', invoice_id)

            # Update invoice status
            if request.form.get('status'):
                status_code = request.form.get('status')
                if db.execute("SELECT * FROM status_code WHERE id = ?", status_code):
                    db.execute("UPDATE invoice SET status = ?, status_date = ? WHERE id = ?", status_code, datetime.now().date(), invoice_id)
                return redirect(url_for('invoices'))

        else:
            flash("Error, invalid input", "error")

    invoices = db.execute("SELECT * FROM invoice WHERE user_id = ? ORDER BY last_saved DESC", session['id'])
    statuses = db.execute("SELECT * FROM status_code")
    return render_template("invoices.html", invoices=invoices, statuses=statuses)


@app.route("/invoices/create", methods=['POST'])
@login_and_verification_required
def create_invoice():
    if request.method == 'POST':
        # Create a template invoice with user info & quotation name
        invoice_name = request.form.get('invoice_name')
        userdata = db.execute("SELECT * FROM user WHERE id = ?", session['id'])[0]
        invoice_id = db.execute("INSERT INTO invoice (user_id, title, sender_name, sender_details) VALUES (?, ?, ?, ?)", userdata['id'], invoice_name, userdata['name'], userdata['details'])
        db.execute("INSERT INTO invoice_items (invoice_id, table_index, unit, rate) VALUES (?, ?, ?, ?)", invoice_id, '01', '1', '0.00')

        return redirect(url_for('view_invoice', invoice_id=invoice_id))


@app.route("/invoices/<int:invoice_id>", methods=['GET', 'POST'])
@login_and_verification_required
def view_invoice(invoice_id):
    # Validate if user is authorised to see this quote, otherwise go back to quote overview page
    user_id = db.execute("SELECT user_id FROM invoice WHERE id = ?", invoice_id)
    if len(user_id) != 1 or user_id[0]['user_id'] != session['id']:
        return redirect(url_for('invoices'))

    if request.method == 'POST':
        # Update and submit details of invoice by user
        form = dict(request.form.items())
        db.execute("""UPDATE invoice
                      SET sender_name=?, sender_details=?, recipient_details=?, project_details=?, send_date=?, ref=?, due_date=?, total_money=?, footnote=?, last_saved=?
                      WHERE id = ?""",
                      form['sender-name'], form['sender-details'], form['recipient-details'], form['project-details'], form['send-date'], form['ref'], form['due-date'], form['total-money'], form['footnote'], datetime.now(),
                      invoice_id)

        # Update table rows for this invoice
        db.execute("DELETE FROM invoice_items WHERE invoice_id = ?", invoice_id)
        for name in request.form:
            if 'row' in name:
                row = request.form.getlist(name)
                db.execute("INSERT INTO invoice_items (invoice_id, table_index, table_description, unit, rate, total) VALUES (?, ?, ?, ?, ?, ?)", invoice_id, row[0], row[1], row[2], row[3], row[4])

    invoice_details = db.execute("SELECT * FROM invoice WHERE id = ?", invoice_id)[0]
    invoice_items = db.execute("SELECT * FROM invoice_items WHERE invoice_id = ? ORDER BY table_index", invoice_id)
    return render_template("view_invoice.html", details=invoice_details, items=invoice_items)

@app.route("/accountsettings", methods=['GET', 'POST'])
def accountsettings():
    if request.method == 'POST':
        db.execute("UPDATE user SET name=?, details=? WHERE id = ?", request.form.get("acc-name"), request.form.get("acc-details"), session['id'])
        flash("Your details have been updated!", "info")
    user_details = db.execute("SELECT * FROM user WHERE id = ?", session['id'])[0]
    return render_template('accountsettings.html', user=user_details)


@app.route("/accountsettings/password", methods=['GET', 'POST'])
def change_password():
    reset_form = ResetForm(request.form, prefix="reset_")

    if request.method == 'POST':
        # Backend form validation
        if not reset_form.validate():
            flash("Please ensure valid input", "error")
            return render_template("changepassword.html", reset_form=reset_form)

        # Check user inputs for duplicate or invalid passwords
        user_pw = db.execute("SELECT password FROM user WHERE id = ?", session['id'])[0]['password']

        if not check_password_hash(user_pw, reset_form.old.data):
            reset_form.old.errors.append("Invalid password!")
        elif reset_form.old.data == reset_form.new.data:
            msg="Passwords are the same!"
            reset_form.old.errors.append(msg)
            reset_form.new.errors.append(msg)
        elif not reset_form.new.data == reset_form.confirm.data:
            msg="Passwords do not match!"
            reset_form.new.errors.append(msg)
            reset_form.confirm.errors.append(msg)
        else:
            new_pw = generate_password_hash(reset_form.new.data)
            db.execute("UPDATE user SET password = ? WHERE id= ?", new_pw, session['id'])
            flash("Password successfully changed", "info")

    return render_template("changepassword.html", reset_form=reset_form)

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.clear()
    flash("Log out successful!", "info")
    return redirect(url_for('index'))

