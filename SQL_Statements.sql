BEGIN;
--
-- Create model Account
--
CREATE TABLE "home_account" ("iban" varchar(34) NOT NULL PRIMARY KEY, "type" integer NOT NULL, "name" varchar(30) NOT NULL, "amount" real NOT NULL, "interest" real NOT NULL, "negative_interest" real NOT NULL, "status" integer NOT NULL);
--
-- Create model Bank
--
CREATE TABLE "home_bank" ("balance" real NOT NULL, "profit" real NOT NULL, "bic" varchar(11) NOT NULL PRIMARY KEY, "name" varchar(30) NOT NULL);        
--
-- Create model BankStatement
--
CREATE TABLE "home_bankstatement" ("id" integer NOT NULL PRIMARY KEY, "time" datetime NOT NULL);
--
-- Create model Employee
--
CREATE TABLE "home_employee" ("eid" integer NOT NULL PRIMARY KEY);
--
-- Create model Transaction
--
CREATE TABLE "home_transaction" ("id" integer NOT NULL PRIMARY KEY, "standing_order" bool NOT NULL, "standing_order_days" integer NULL, "time_of_transac
tion" datetime NOT NULL, "amount" real NOT NULL, "receiving_account" varchar(34) NOT NULL, "receiving_name" varchar(30) NULL, "usage" varchar(140) NULL,
 "approved" bool NOT NULL, "approved_by_id" integer NULL REFERENCES "home_employee" ("eid") DEFERRABLE INITIALLY DEFERRED, "sending_account_id" varchar(34) NOT NULL REFERENCES "home_account" ("iban") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Tan
--
CREATE TABLE "home_tan" ("tan" integer NOT NULL PRIMARY KEY, "state" bool NOT NULL, "account_id" varchar(34) NOT NULL REFERENCES "home_account" ("iban") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Person
--
CREATE TABLE "home_person" ("user_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "profile_picture" varchar(100) NULL, "address" varchar(100) NOT NULL, "phone_number" varchar(20) NULL, "birthday" date NOT NULL);
CREATE TABLE "home_person_contacts" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "from_person_id" integer NOT NULL REFERENCES "home_person" ("user_ptr_id") DEFERRABLE INITIALLY DEFERRED, "to_person_id" integer NOT NULL REFERENCES "home_person" ("user_ptr_id") DEFERRABLE INITIALLY DEFERRED);        
--
-- Add field person to employee
--
CREATE TABLE "new__home_employee" ("eid" integer NOT NULL PRIMARY KEY, "person_id" integer NOT NULL REFERENCES "home_person" ("user_ptr_id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "new__home_employee" ("eid", "person_id") SELECT "eid", NULL FROM "home_employee";
DROP TABLE "home_employee";
ALTER TABLE "new__home_employee" RENAME TO "home_employee";
CREATE INDEX "home_transaction_approved_by_id_baa8075e" ON "home_transaction" ("approved_by_id");
CREATE INDEX "home_transaction_sending_account_id_80df477c" ON "home_transaction" ("sending_account_id");
CREATE INDEX "home_tan_account_id_554c4e75" ON "home_tan" ("account_id");
CREATE UNIQUE INDEX "home_person_contacts_from_person_id_to_person_id_968d7663_uniq" ON "home_person_contacts" ("from_person_id", "to_person_id");      
CREATE INDEX "home_person_contacts_from_person_id_bddcf467" ON "home_person_contacts" ("from_person_id");
CREATE INDEX "home_person_contacts_to_person_id_95e9920e" ON "home_person_contacts" ("to_person_id");
CREATE INDEX "home_employee_person_id_45895482" ON "home_employee" ("person_id");
--
-- Create model DebitCard
--
CREATE TABLE "home_debitcard" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "pin" integer NOT NULL, "state" bool NOT NULL, "expiration_date" date NOT NULL, "account_id" varchar(34) NOT NULL REFERENCES "home_account" ("iban") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Card
--
CREATE TABLE "home_card" ("id" varchar(30) NOT NULL PRIMARY KEY, "cvv" integer NOT NULL, "pin" integer NOT NULL, "state" bool NOT NULL, "expiration_date" date NOT NULL, "account_id" varchar(34) NOT NULL REFERENCES "home_account" ("iban") DEFERRABLE INITIALLY DEFERRED);
--
-- Add field employee to account
--
ALTER TABLE "home_account" ADD COLUMN "employee_id" integer NULL REFERENCES "home_employee" ("eid") DEFERRABLE INITIALLY DEFERRED;
--
-- Add field owner to account
--
ALTER TABLE "home_account" ADD COLUMN "owner_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "home_debitcard_account_id_aa99968b" ON "home_debitcard" ("account_id");
CREATE INDEX "home_card_account_id_bb57ae1a" ON "home_card" ("account_id");
CREATE INDEX "home_account_employee_id_e89cdef0" ON "home_account" ("employee_id");
CREATE INDEX "home_account_owner_id_148f1ca9" ON "home_account" ("owner_id");
COMMIT;
(venv) PS C:\Users\agaja\PycharmProjects\db-praktikum-a06\megagutebank> python manage.py sqlmigrate home 0001
BEGIN;
--
-- Create model Account
--
CREATE TABLE "home_account" ("iban" varchar(34) NOT NULL PRIMARY KEY, "type" integer NOT NULL, "name" varchar(30) NOT NULL, "amount" real NOT NULL, "interest" real NOT NULL, "negative_interest" real NOT NULL, "status" integer NOT NULL);
--
-- Create model Bank
--
CREATE TABLE "home_bank" ("balance" real NOT NULL, "profit" real NOT NULL, "bic" varchar(11) NOT NULL PRIMARY KEY, "name" varchar(30) NOT NULL);        
--
-- Create model BankStatement
--
CREATE TABLE "home_bankstatement" ("id" integer NOT NULL PRIMARY KEY, "time" datetime NOT NULL);
--
-- Create model Employee
--
CREATE TABLE "home_employee" ("eid" integer NOT NULL PRIMARY KEY);
--
-- Create model Transaction
--
CREATE TABLE "home_transaction" ("id" integer NOT NULL PRIMARY KEY, "standing_order" bool NOT NULL, "standing_order_days" integer NULL, "time_of_transac
tion" datetime NOT NULL, "amount" real NOT NULL, "receiving_account" varchar(34) NOT NULL, "receiving_name" varchar(30) NULL, "usage" varchar(140) NULL,
 "approved" bool NOT NULL, "approved_by_id" integer NULL REFERENCES "home_employee" ("eid") DEFERRABLE INITIALLY DEFERRED, "sending_account_id" varchar(34) NOT NULL REFERENCES "home_account" ("iban") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Tan
--
CREATE TABLE "home_tan" ("tan" integer NOT NULL PRIMARY KEY, "state" bool NOT NULL, "account_id" varchar(34) NOT NULL REFERENCES "home_account" ("iban") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Person
--
CREATE TABLE "home_person" ("user_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "profile_picture" varchar(100) NULL, "address" varchar(100) NOT NULL, "phone_number" varchar(20) NULL, "birthday" date NOT NULL);
CREATE TABLE "home_person_contacts" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "from_person_id" integer NOT NULL REFERENCES "home_person" ("user_ptr_id") DEFERRABLE INITIALLY DEFERRED, "to_person_id" integer NOT NULL REFERENCES "home_person" ("user_ptr_id") DEFERRABLE INITIALLY DEFERRED);        
--
-- Add field person to employee
--
CREATE TABLE "new__home_employee" ("eid" integer NOT NULL PRIMARY KEY, "person_id" integer NOT NULL REFERENCES "home_person" ("user_ptr_id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "new__home_employee" ("eid", "person_id") SELECT "eid", NULL FROM "home_employee";
DROP TABLE "home_employee";
ALTER TABLE "new__home_employee" RENAME TO "home_employee";
CREATE INDEX "home_transaction_approved_by_id_baa8075e" ON "home_transaction" ("approved_by_id");
CREATE INDEX "home_transaction_sending_account_id_80df477c" ON "home_transaction" ("sending_account_id");
CREATE INDEX "home_tan_account_id_554c4e75" ON "home_tan" ("account_id");
CREATE UNIQUE INDEX "home_person_contacts_from_person_id_to_person_id_968d7663_uniq" ON "home_person_contacts" ("from_person_id", "to_person_id");      
CREATE INDEX "home_person_contacts_from_person_id_bddcf467" ON "home_person_contacts" ("from_person_id");
CREATE INDEX "home_person_contacts_to_person_id_95e9920e" ON "home_person_contacts" ("to_person_id");
CREATE INDEX "home_employee_person_id_45895482" ON "home_employee" ("person_id");
--
-- Create model DebitCard
--
CREATE TABLE "home_debitcard" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "pin" integer NOT NULL, "state" bool NOT NULL, "expiration_date" date NOT NULL, "account_id" varchar(34) NOT NULL REFERENCES "home_account" ("iban") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Card
--
CREATE TABLE "home_card" ("id" varchar(30) NOT NULL PRIMARY KEY, "cvv" integer NOT NULL, "pin" integer NOT NULL, "state" bool NOT NULL, "expiration_date" date NOT NULL, "account_id" varchar(34) NOT NULL REFERENCES "home_account" ("iban") DEFERRABLE INITIALLY DEFERRED);
--
-- Add field employee to account
--
ALTER TABLE "home_account" ADD COLUMN "employee_id" integer NULL REFERENCES "home_employee" ("eid") DEFERRABLE INITIALLY DEFERRED;
--
-- Add field owner to account
--
ALTER TABLE "home_account" ADD COLUMN "owner_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "home_debitcard_account_id_aa99968b" ON "home_debitcard" ("account_id");
CREATE INDEX "home_card_account_id_bb57ae1a" ON "home_card" ("account_id");
CREATE INDEX "home_account_employee_id_e89cdef0" ON "home_account" ("employee_id");
CREATE INDEX "home_account_owner_id_148f1ca9" ON "home_account" ("owner_id");
COMMIT;
