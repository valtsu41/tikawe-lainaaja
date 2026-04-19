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
    author INTEGER REFERENCES Users,
    item TEXT,
    info TEXT
);

CREATE TABLE Views (
    id INTEGER PRIMARY KEY,
    viewed_at TEXT,
    user INTEGER REFERENCES Users,
    post INTEGER REFERENCES Posts
)