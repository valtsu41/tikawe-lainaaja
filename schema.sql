CREATE TABLE Visits (
    id INTEGER PRIMARY KEY,
    visited_at TEXT
);

CREATE TABLE Users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE Categories (
    id INTEGER PRIMARY KEY,
    name TEXT
);


CREATE TABLE Posts (
    id INTEGER PRIMARY KEY,
    author INTEGER REFERENCES Users,
    item TEXT,
    category INTEGER REFERENCES Categories ON DELETE SET NULL,
    info TEXT
);

CREATE TABLE Views (
    id INTEGER PRIMARY KEY,
    viewed_at TEXT,
    user INTEGER REFERENCES Users,
    post INTEGER REFERENCES Posts ON DELETE CASCADE
);

CREATE TABLE Reservations (
    id INTEGER PRIMARY KEY,
    post INTEGER REFERENCES Posts ON DELETE CASCADE,
    user INTEGER REFERENCES Users,
    start_date TEXT,
    end_date TEXT
);