DO $$
DECLARE
    jid integer;
    scid integer;
BEGIN
-- Creating a new job
INSERT INTO pgagent.pga_job(
    jobjclid, jobname, jobdesc, jobhostagent, jobenabled
) VALUES (
    1::integer, 'Bilanz'::text, ''::text, ''::text, true
) RETURNING jobid INTO jid;

-- Steps
-- Inserting a step (jobid: NULL)
INSERT INTO pgagent.pga_jobstep (
    jstjobid, jstname, jstenabled, jstkind,
    jstconnstr, jstdbname, jstonerror,
    jstcode, jstdesc
) VALUES (
    jid, 'UpdateBilanz'::text, true, 's'::character(1),
    ''::text, 'postgres'::name, 'f'::character(1),
    'UPDATE home_bank
SET balance = (SELECT sum(amount)
			  FROM home_account)'::text, ''::text
) ;

-- Schedules
-- Inserting a schedule
INSERT INTO pgagent.pga_schedule(
    jscjobid, jscname, jscdesc, jscenabled,
    jscstart, jscend,    jscminutes, jschours, jscweekdays, jscmonthdays, jscmonths
) VALUES (
    jid, 'ScheduleBilanz'::text, ''::text, true,
    '2022-10-10 00:00:00+02'::timestamp with time zone, '2023-10-10 00:00:00+02'::timestamp with time zone,
    -- Minutes
    ARRAY[true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true]::boolean[],
    -- Hours
    ARRAY[true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true]::boolean[],
    -- Week days
    ARRAY[true,true,true,true,true,true,true]::boolean[],
    -- Month days
    ARRAY[false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false]::boolean[],
    -- Months
    ARRAY[false,false,false,false,false,false,false,false,false,false,false,false]::boolean[]
) RETURNING jscid INTO scid;
END
$$;

DO $$
DECLARE
    jid integer;
    scid integer;
BEGIN
-- Creating a new job
INSERT INTO pgagent.pga_job(
    jobjclid, jobname, jobdesc, jobhostagent, jobenabled
) VALUES (
    1::integer, 'Zinsen/Profit'::text, ''::text, ''::text, true
) RETURNING jobid INTO jid;

-- Steps
-- Inserting a step (jobid: NULL)
INSERT INTO pgagent.pga_jobstep (
    jstjobid, jstname, jstenabled, jstkind,
    jstconnstr, jstdbname, jstonerror,
    jstcode, jstdesc
) VALUES (
    jid, 'UpdateZinsenProfit'::text, true, 's'::character(1),
    ''::text, 'postgres'::name, 'f'::character(1),
    'UPDATE home_bank
SET profit = profit -
    		  (SELECT sum(round(amount * ((POWER(1 + interest, (1/12.0)) - 1))::numeric, 2)::float)
			  FROM home_account
		      WHERE amount >= 0)
			   +
			  (SELECT sum(round(amount * ((POWER(1 - negative_interest, (1/12.0)) - 1))::numeric, 2)::float)
			  FROM home_account
		      WHERE amount < 0);

UPDATE home_account
SET amount = round(amount::numeric + (amount * ((POWER(1 + interest, (1/12.0)) - 1)))::numeric, 2)::float
WHERE amount >= 0;

UPDATE home_account
SET amount = round(amount::numeric + (amount * ((POWER(1 - negative_interest, (1/12.0)) - 1)))::numeric, 2)::float
WHERE amount < 0;'::text, ''::text
) ;

-- Schedules
-- Inserting a schedule
INSERT INTO pgagent.pga_schedule(
    jscjobid, jscname, jscdesc, jscenabled,
    jscstart, jscend,    jscminutes, jschours, jscweekdays, jscmonthdays, jscmonths
) VALUES (
    jid, 'ScheduleZinsenProfit'::text, ''::text, true,
    '2022-10-10 00:00:00+02'::timestamp with time zone, '2023-10-10 00:00:00+02'::timestamp with time zone,
    -- Minutes
    ARRAY[true,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false]::boolean[],
    -- Hours
    ARRAY[true,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false]::boolean[],
    -- Week days
    ARRAY[false,false,false,false,false,false,false]::boolean[],
    -- Month days
    ARRAY[true,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false]::boolean[],
    -- Months
    ARRAY[true,true,true,true,true,true,true,true,true,true,true,true]::boolean[]
) RETURNING jscid INTO scid;
END
$$;

DO $$
DECLARE
    jid integer;
    scid integer;
BEGIN
-- Creating a new job
INSERT INTO pgagent.pga_job(
    jobjclid, jobname, jobdesc, jobhostagent, jobenabled
) VALUES (
    1::integer, 'Renew Card'::text, ''::text, ''::text, true
) RETURNING jobid INTO jid;

-- Steps
-- Inserting a step (jobid: NULL)
INSERT INTO pgagent.pga_jobstep (
    jstjobid, jstname, jstenabled, jstkind,
    jstconnstr, jstdbname, jstonerror,
    jstcode, jstdesc
) VALUES (
    jid, 'AddNewCard'::text, true, 's'::character(1),
    ''::text, 'postgres'::name, 'f'::character(1),
    'UPDATE home_card
SET expiration_date = now() + interval ''1826.2125  days''
WHERE expiration_date - interval ''14 days'' < now()'::text, ''::text
) ;

-- Schedules
-- Inserting a schedule
INSERT INTO pgagent.pga_schedule(
    jscjobid, jscname, jscdesc, jscenabled,
    jscstart, jscend,    jscminutes, jschours, jscweekdays, jscmonthdays, jscmonths
) VALUES (
    jid, 'card_schedule'::text, ''::text, true,
    '2022-10-07 00:00:00+02'::timestamp with time zone, '2023-10-07 00:00:00+02'::timestamp with time zone,
    -- Minutes
    ARRAY[true,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false]::boolean[],
    -- Hours
    ARRAY[true,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false]::boolean[],
    -- Week days
    ARRAY[true,true,true,true,true,true,true]::boolean[],
    -- Month days
    ARRAY[false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false]::boolean[],
    -- Months
    ARRAY[false,false,false,false,false,false,false,false,false,false,false,false]::boolean[]
) RETURNING jscid INTO scid;
END
$$;

DO $$
DECLARE
    jid integer;
    scid integer;
BEGIN
-- Creating a new job
INSERT INTO pgagent.pga_job(
    jobjclid, jobname, jobdesc, jobhostagent, jobenabled
) VALUES (
    1::integer, 'standing_order'::text, ''::text, ''::text, true
) RETURNING jobid INTO jid;

-- Steps
-- Inserting a step (jobid: NULL)
INSERT INTO pgagent.pga_jobstep (
    jstjobid, jstname, jstenabled, jstkind,
    jstconnstr, jstdbname, jstonerror,
    jstcode, jstdesc
) VALUES (
    jid, 'AddMoneyReceiver'::text, true, 's'::character(1),
    ''::text, 'postgres'::name, 'f'::character(1),
    'UPDATE home_account
SET amount = home_account.amount + inner_query.amount
FROM (SELECT iban_receiver, SUM(amount) as amount
FROM home_transaction
WHERE standing_order = True
AND timestamp + INTERVAL ''1'' day * standing_order_days < now()
GROUP BY iban_receiver) as inner_query
WHERE home_account.iban = inner_query.iban_receiver;'::text, 'Add Money to receivers bank account'::text
) ;-- Inserting a step (jobid: NULL)
INSERT INTO pgagent.pga_jobstep (
    jstjobid, jstname, jstenabled, jstkind,
    jstconnstr, jstdbname, jstonerror,
    jstcode, jstdesc
) VALUES (
    jid, 'DoubleStandingOrderTime'::text, true, 's'::character(1),
    ''::text, 'postgres'::name, 'f'::character(1),
    'UPDATE home_transaction
SET standing_order_days = standing_order_days * 2
WHERE timestamp + INTERVAL ''1'' day * standing_order_days < now()
AND standing_order IS True;'::text, 'Double every standing order time'::text
) ;-- Inserting a step (jobid: NULL)
INSERT INTO pgagent.pga_jobstep (
    jstjobid, jstname, jstenabled, jstkind,
    jstconnstr, jstdbname, jstonerror,
    jstcode, jstdesc
) VALUES (
    jid, 'RemoveMoneyFromSender'::text, true, 's'::character(1),
    ''::text, 'postgres'::name, 'f'::character(1),
    'UPDATE home_account
SET amount = home_account.amount - inner_query.amount
FROM (SELECT iban_sender_id, SUM(amount) as amount
FROM home_transaction
WHERE standing_order = True
AND timestamp + INTERVAL ''1'' day * standing_order_days < now()
GROUP BY iban_sender_id) as inner_query
WHERE home_account.iban = inner_query.iban_sender_id;'::text, 'Change Senders Bank Accounts Amount -transaction amount'::text
) ;

-- Schedules
-- Inserting a schedule
INSERT INTO pgagent.pga_schedule(
    jscjobid, jscname, jscdesc, jscenabled,
    jscstart,     jscminutes, jschours, jscweekdays, jscmonthdays, jscmonths
) VALUES (
    jid, 'daily'::text, ''::text, true,
    '2022-09-29 09:12:00+02'::timestamp with time zone, 
    -- Minutes
    ARRAY[true,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false]::boolean[],
    -- Hours
    ARRAY[true,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false]::boolean[],
    -- Week days
    ARRAY[true,true,true,true,true,true,true]::boolean[],
    -- Month days
    ARRAY[true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true]::boolean[],
    -- Months
    ARRAY[true,true,true,true,true,true,true,true,true,true,true,true]::boolean[]
) RETURNING jscid INTO scid;
END
$$;