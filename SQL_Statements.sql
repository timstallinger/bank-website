BEGIN;
--
-- Create model Account
--
CREATE TABLE "account" (
	"iban" varchar(34) NOT NULL PRIMARY KEY, 
	"type" integer NOT NULL, 
	"name" varchar(30) NOT NULL, 
	"amount" real NOT NULL, 
	"interest" real NOT NULL, 
	"negative_interest" real NOT NULL, 
	"status" integer NOT NULL
);
--
-- Create model AccountKopie
--
CREATE TABLE "accountkopie" (
	"iban" varchar(34) NOT NULL PRIMARY KEY, 
	"type" integer NOT NULL, 
	"name" varchar(30) NOT NULL, 
	"amount" real NOT NULL, 
	"interest" real NOT NULL, 
	"negative_interest" real NOT NULL, 
	"status" integer NOT NULL
);
--
-- Create model Bank
--
CREATE TABLE "bank" (
	"balance" real NOT NULL, 
	"profit" real NOT NULL, 
	"bic" varchar(11) NOT NULL PRIMARY KEY, 
	"name" varchar(30) NOT NULL
);        
--
-- Create model BankStatement
--
CREATE TABLE "bankstatement" (
	"id" integer NOT NULL PRIMARY KEY, 
	"time" datetime NOT NULL
);
--
-- Create model Transaction
--
CREATE TABLE "transaction" (
	"id" integer NOT NULL PRIMARY KEY, 
	"standing_order" bool NOT NULL, 
	"standing_order_days" integer NULL, 
	"time_of_transaction" datetime NOT NULL, 
	"amount" real NOT NULL, 
	"receiving_account" varchar(34) NOT NULL, 
	"receiving_name" varchar(30) NULL, 
	"usage" varchar(140) NULL,
	"approved" bool NOT NULL, 
	"approved_by_id" integer NULL REFERENCES "employee" ("eid") DEFERRABLE INITIALLY DEFERRED, 
	"sending_account_id" varchar(34) NOT NULL REFERENCES "account" ("iban") DEFERRABLE INITIALLY DEFERRED
);
--
-- Create model Tan
--
CREATE TABLE "tan" (
	"tan" integer NOT NULL PRIMARY KEY, 
	"state" bool NOT NULL, 
	"account_id" varchar(34) NOT NULL REFERENCES "account" ("iban") DEFERRABLE INITIALLY DEFERRED
);
--
-- Create model Person. Person erbt von User. User ist von Django vorgegeben mit Datenfeldern wie Username, Password.
--
CREATE TABLE "person" (
	"user_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, 
	"profile_picture" varchar(100) NULL, 
	"address" varchar(100) NOT NULL, 
	"phone_number" varchar(20) NULL, 
	"birthday" date NOT NULL
);
CREATE TABLE "person_contacts" (
	"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
	"from_person_id" integer NOT NULL REFERENCES "person" ("user_ptr_id") DEFERRABLE INITIALLY DEFERRED, 
	"to_person_id" integer NOT NULL REFERENCES "person" ("user_ptr_id") DEFERRABLE INITIALLY DEFERRED
);        
--
-- Add field person to employee
--
CREATE TABLE "employee" (
	"eid" integer NOT NULL PRIMARY KEY, 
	"person_id" integer NOT NULL REFERENCES "person" ("user_ptr_id") DEFERRABLE INITIALLY DEFERRED
);
--
-- Create model DebitCard
--
CREATE TABLE "debitcard" (
	"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
	"pin" integer NOT NULL, "state" bool NOT NULL, 
	"expiration_date" date NOT NULL, 
	"account_id" varchar(34) NOT NULL REFERENCES "account" ("iban") DEFERRABLE INITIALLY DEFERRED
);
--
-- Create model Card
--
CREATE TABLE "card" (
	"id" varchar(30) NOT NULL PRIMARY KEY, 
	"cvv" integer NOT NULL, 
	"pin" integer NOT NULL, 
	"state" bool NOT NULL, 
	"expiration_date" date NOT NULL, 
	"account_id" varchar(34) NOT NULL REFERENCES "account" ("iban") DEFERRABLE INITIALLY DEFERRED
);
COMMIT;
