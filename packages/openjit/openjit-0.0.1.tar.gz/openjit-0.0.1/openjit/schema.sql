-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS lane;
DROP TABLE IF EXISTS card;

CREATE TABLE lane (
        id INTEGER PRIMARY KEY,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT NULL,
        title TEXT UNIQUE NOT NULL,
        slug TEXT UNIQUE NOT NULL
);

INSERT INTO lane (slug, title) VALUES
        ("backlog", "Backlog"),
        ("doing", "Doing"),
        ("review", "Review"),
        ("done", "Done");

CREATE TABLE card (
        id INTEGER PRIMARY KEY,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT NULL,
        title TEXT UNIQUE NOT NULL,
        description TEXT NOT NULL,
        lane_id INTEGER NOT NULL,
        FOREIGN KEY(lane_id) REFERENCES lane(id) ON DELETE NO ACTION ON UPDATE NO ACTION
);
