-- schema.sql
-- Drop tables if already exists
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS asset;


-- Drop views if already exists
DROP VIEW IF EXISTS user_asset;


-- Create tables
CREATE TABLE user (
    uid VARCHAR (28) PRIMARY KEY,
    email VARCHAR (64) NOT NULL UNIQUE,
    capital FLOAT NOT NULL DEFAULT 500000
);

CREATE TABLE asset (
    uid VARCHAR (28) REFERENCES user (uid),
    label VARCHAR (16) NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    bought DATE NOT NULL,
    price FLOAT NOT NULL,
    slp FLOAT NOT NULL DEFAULT 0
);


-- Create views
CREATE VIEW user_asset AS
     SELECT user.uid,
            email,
            capital,
            label,
            quantity,
            bought,
            price,
            slp
       FROM asset
 INNER JOIN user
         ON user.uid = asset.uid;
