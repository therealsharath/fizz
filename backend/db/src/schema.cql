-- schema.cql
-- Drop tables if already exists
DROP TABLE IF EXISTS "pkid";
DROP TABLE IF EXISTS "user";
DROP TABLE IF EXISTS "asset";


-- Create tables
CREATE TABLE "pkid" (
    "label" VARCHAR PRIMARY KEY,
    "id" COUNTER
);

CREATE TABLE "user" (
    "id" INT PRIMARY KEY,
    "uid" VARCHAR,
    "email" VARCHAR
);

CREATE TABLE "asset" (
    "id" INT PRIMARY KEY,
    "uid" VARCHAR,
    "label" VARCHAR,
    "quantity" INT,
    "bought" TIMESTAMP
);
