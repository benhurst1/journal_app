CREATE SCHEMA journal_app;

CREATE TABLE "users" (
  "id" SERIAL PRIMARY KEY,
  "username" varchar(20),
  "email" varchar(50),
  "password" varchar(30)
);

CREATE TABLE "posts" (
  "id" SERIAL PRIMARY KEY,
  "user_id" integer,
  "title" varchar,
  "body" text,
  "created_at" timestamp,
  "last_edited" timestamp,
  "published" BOOLEAN
);

ALTER TABLE "posts" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");
