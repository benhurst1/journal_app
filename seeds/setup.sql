CREATE EXTENSION citext;
CREATE DOMAIN email AS citext
CHECK(
   VALUE ~ '^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$'
);


CREATE TABLE "users" (
  "id" SERIAL PRIMARY KEY,
  "username" varchar(20) UNIQUE NOT NULL,
  "email" email UNIQUE NOT NULL,
  "password" BYTEA NOT NULL
) ;

CREATE TABLE "posts" (
  "id" SERIAL PRIMARY KEY,
  "user_id" integer,
  "title" varchar,
  "body" text,
  "created_at" timestamp,
  "last_edited" timestamp,
  "published" BOOLEAN
) ;

ALTER TABLE "posts" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");