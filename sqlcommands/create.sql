CREATE TABLE user
(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL,
    name TEXT NOT NULL,
    address TEXT,
    details TEXT
);

CREATE TABLE quote
(
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    last_saved TEXT NOT NULL
        DEFAULT (CURRENT_TIMESTAMP),
    title TEXT NOT NULL,
    sender_name TEXT NOT NULL,
    sender_details TEXT,
    recipient_details TEXT NOT NULL
        DEFAULT '[Recipient Details Here]',
    project_details TEXT NOT NULL
        DEFAULT '[Project Details Here]',
    send_date TEXT
        DEFAULT CURRENT_DATE,
    ref TEXT NOT NULL
        DEFAULT '[Reference No.]',
    valid_till TEXT
        DEFAULT '[Validity Date]',
    footnote TEXT
        DEFAULT '[Additional Information]',
    total_money TEXT NOT NULL
        DEFAULT '0',
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);

CREATE TABLE quote_items
(
    id INTEGER PRIMARY KEY,
    quote_id INTEGER NOT NULL,
    table_index INTEGER,
    table_description TEXT,
    unit INTEGER,
    rate INTEGER,
    total INTEGER,
    FOREIGN KEY (quote_id) REFERENCES quote(id) ON DELETE CASCADE
);

CREATE TABLE quote_items
(
    id INTEGER PRIMARY KEY,
    quote_id INTEGER NOT NULL,
    table_index TEXT
        DEFAULT '01',
    table_description TEXT
        DEFAULT '[Line Item Here]',
    unit INTEGER
        DEFAULT '1',
    rate INTEGER
        DEFAULT '0',
    total INTEGER
        DEFAULT '0',
    FOREIGN KEY (quote_id) REFERENCES quote(id) ON DELETE CASCADE
);

CREATE TABLE invoice
(
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    last_saved TEXT NOT NULL
        DEFAULT (CURRENT_TIMESTAMP),
    title TEXT NOT NULL,
    sender_name TEXT NOT NULL,
    sender_details TEXT,
    recipient_details TEXT NOT NULL
        DEFAULT '[Recipient Details Here]',
    project_details TEXT NOT NULL
        DEFAULT '[Project Details Here]',
    send_date TEXT
        DEFAULT CURRENT_DATE,
    ref TEXT NOT NULL
        DEFAULT '[Reference No.]',
    due_date TEXT
        DEFAULT '[Due Date]',
    footnote TEXT
        DEFAULT '[Additional Information]',
    total_money TEXT NOT NULL
        DEFAULT '0',
    status INTEGER NOT NULL
        DEFAULT 1,
    status_date TEXT
        DEFAULT CURRENT_DATE,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
    FOREIGN KEY (status) REFERENCES status_code(id)
);

CREATE TABLE invoice_items
(
    id INTEGER PRIMARY KEY,
    invoice_id INTEGER NOT NULL,
    table_index TEXT
        DEFAULT '01',
    table_description TEXT
        DEFAULT '[Line Item Here]',
    unit INTEGER
        DEFAULT '1',
    rate INTEGER
        DEFAULT '0',
    total INTEGER
        DEFAULT '0',
    FOREIGN KEY (invoice_id) REFERENCES invoice(id) ON DELETE CASCADE
);

CREATE TABLE status_code
(
    id INTEGER PRIMARY KEY,
    status TEXT NOT NULL
);

CREATE TABLE otp
(
    user_id INTEGER PRIMARY KEY,
    otp INTEGER NOT NULL,
    timestamp TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);