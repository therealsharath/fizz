-- populate.cql
-- Delete existing data in tables
DELETE FROM "pkid";


-- Insert data into tables
UPDATE "pkid" SET "id" = "id" + 1 WHERE "label" = 'user';
UPDATE "pkid" SET "id" = "id" + 1 WHERE "label" = 'asset';