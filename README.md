# invoicer.
> CS50x 2022 Final Project

**invoicer.** is a web-based application that allows users to generate quotations and invoices, convert quotations to invoices and keep track of their invoice payments.

*Video Link: https://youtu.be/hgapzd9CuKc*

## Features
- Register and Login
    - To register for an account, users will be prompted to enter the following: username, password, email, name and company details.
    - Users will then be prompted to the email verification page upon login. Access to the application features will not be granted before completing the email verification.
    - A One-Time-Password (OTP) will be sent to the registered email for verification. The OTP will only be valid for 10 minutes. Users may choose to request for another OTP if theirs have expired.


- Home Page
    - Upon login, users will see a brief summary of their quotations and invoices. It includes:
        - Number of unpaid invoices and their total amount
        - Five most recent quotations and invoices
    - They may choose to access these recent files directly via the homepage.


- Side Bar
    - Users may choose to create a new quotation/invoice, view their current quotations/invoices, access their account settings or log out.


- View Quotations Page
    - In a table format, users will be able to see all their quotations in reverse chronological order.
    - Buttons in the form of icons allow users to easily create new quotation, edit quotation name, duplicate or delete a quotation. The *invoicer.* icon allows users to convert the quotation to an invoice, which will be added to their invoices tab.
    - Users may click on any of the table rows to view that quotation in detail.


- View Invoices Page
    - Similarly to the Quotations tab, users may view, create, edit name, duplicate or delete invoices.
    - Instead of the *invoicer.* icon, users may set a status for their invoice here. The options include "Not Sent Yet", "Pending Payment" and "Payment Received".


- Quotation/Invoice Page
    - Here is where users are able to edit their quotation/invoice details and save them.
    - Thereafter, they may export the file into PDF format.

- Account Settings
    - Users can edit their Name or Company Details directly, or request to change their password.
    - Usernames and emails are unique and cannot be changed after registration.



## Technologies
- Flask (Python)
    - `app.py` handles all the configuration, routing and access for various pages, updating database, making calculations and passing in necessary information for the site to display.
    - `helpers.py` includes
        - Decorator functions that redirect users if login is required or not required (referenced from PSET9 Finance)
        - Classes for WTForms
        - `copy_sqlscripts` runs two specified SQL scripts when user duplicates a file or converts it from quotation to invoice. These queries are particularly long and hence it was not ideal to hardcode it inside `app.py`.
- SQLite
    - The application database includes these tables: user, quote, quote_items, invoice, invoice_items, status_code, otp.

- HTML & CSS
- JavaScript/JQuery
    - Multiple js scripts across the site that handles certain functionalities and design elements.
        - Toggle display of sidebar, display of pop-up boxes (when creating new file).
        - Dynamically calculate total cost, add and delete rows in quotation/invoice items table.
        - Parsing edited ContentEditable text into respective text areas to submit as a form to the server.
    - Utilising external packages like `day.js` and `html2pdf.js`

### External Modules and Packages
- `WTForms` (https://wtforms.readthedocs.io/en/3.0.x/)
    - User input validation and error displaying for the Register, Login and Change Password pages.

- `werkzeug.security` (https://werkzeug.palletsprojects.com/en/2.2.x/utils/)
    - `generate_password_hash` & `check_password_hash`
    - Utility library for password hashing into the database (referenced from PSET9 Finance).

- `Flask Mail` (https://pythonhosted.org/Flask-Mail/)
    - To send user a One-Time-Password for email verification, configured with the SMTP Gmail server.

- `CS50` SQL Library (https://cs50.readthedocs.io/libraries/cs50/python/#cs50.SQL)
    - To perform CRUD operations for the application's database.

- `day.js` (https://day.js.org/)
    - To display relative timewhere users can see how long ago each file was last saved.

- `html2pdf.js` (https://ekoopmans.github.io/html2pdf.js/)
    - To convert the HTML canvas into a PDF file format.

- `autosize` (http://www.jacklmoore.com/autosize/)
    - To adjust textarea height automatically, used for the Register and Account Settings page

- Fonts are from Google Fonts (https://fonts.google.com/) and icons are from Font Awesome (https://fontawesome.com).