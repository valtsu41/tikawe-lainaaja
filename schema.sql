CREATE TABLE Visits (
    id INTEGER PRIMARY KEY,
    visited_at TEXT
);

CREATE TABLE Users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE Posts (
    id INTEGER PRIMARY KEY,
    author TEXT,
    item TEXT
);