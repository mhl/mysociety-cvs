-- 
-- schema.sql:
-- Schema for petitions database.
--
-- Copyright (c) 2006 UK Citizens Online Democracy. All rights reserved.
-- Email: francis@mysociety.org; WWW: http://www.mysociety.org/
--
-- $Id: schema.sql,v 1.19 2006-08-01 08:41:47 chris Exp $
--

-- global_seq
-- Global sequence counter.
create sequence global_seq;

-- secret
-- A random secret.
create table secret (
    secret text not null
);

-- If a row is present, that is date which is "today".  Used for debugging
-- to advance time without having to wait.
create table debugdate (
    override_today date
);

-- Returns the date of "today", which can be overriden for testing.
create function ms_current_date()
    returns date as '
    declare
        today date;
    begin
        today = (select override_today from debugdate);
        if today is not null then
           return today;
        else
           return current_date;
        end if;

    end;
' language 'plpgsql';

-- Returns the timestamp of current time, but with possibly overriden "today".
create function ms_current_timestamp()
    returns timestamp as '
    declare
        today date;
    begin
        today = (select override_today from debugdate);
        if today is not null then
           return today + current_time;
        else
           return current_timestamp;
        end if;
    end;
' language 'plpgsql';

-- information about each petition
create table petition (
    id integer not null primary key default nextval('global_seq'),
    -- short name of petition for URLs
    ref text not null,

    -- summary of petition
    title text not null, -- LLL
    -- "We the undersigned petition the Prime Minister to..."
    content text not null default '', -- LLL
    -- target deadline, midnight at end of this day
    deadline date not null,
    -- actual text entered, just in case parse_date() goes wrong
    rawdeadline text not null,

    -- petition creator
    email text not null,
    name text not null,
    organisation text not null,
    address text not null,
    postcode text not null,
    telephone text not null,
    org_url text not null,

    -- metadata
    creationtime timestamp not null,
    
    status text not null default 'unconfirmed' check (
        status in (
        'unconfirmed',      -- email not yet confirmed
        'draft',            -- waiting for approval
        'rejectedonce',     -- rejected once
        'resubmitted',      -- resubmitted
        'rejected',         -- rejected finally, or timed out
        'live',             -- active
        'finished'          -- deadline passed
        )
    ),

    rejection_first_categories int,
    rejection_first_reason text,
    rejection_second_categories int,
    rejection_second_reason text,

    laststatuschange timestamp not null

    -- add fields to run confirmation email stuff
);

create unique index petition_ref_idx on petition(ref);
create index petition_status_idx on petition(status);

-- History of things which have happened to a petition
create table petition_log (
    order_id integer not null primary key default nextval('global_seq'), -- for ordering
    petition_id integer not null references petition(id),
    whenlogged timestamp not null,
    message text not null,
    editor text -- administrator who performed this action, or NULL
);

create table signer (
    id integer not null primary key default nextval('global_seq'),
    petition_id integer not null references petition(id),

    -- Who has signed the petition.
    email text not null,
    name text not null,
    address text not null,
    postcode text not null,

    -- whether this signer is included in the petition or not
    showname boolean not null default false,
      
    -- when they signed
    signtime timestamp not null,

    -- has the confirmation mail been sent to the user, and have they
    -- clicked the confirm link?
    emailsent text not null default ('pending') check (
        emailsent in (
        'pending',          -- not sent yet
        'sent',             -- successfully sent
        'failed',           -- permanent failure
        'confirmed'         -- confirm link clicked
        )
    )
);

create index signer_petition_id_idx on signer(petition_id);
create unique index signer_petition_id_email_idx on signer(petition_id, email);
create index signer_emailsent_idx on signer(emailsent);

-- petition_is_valid_to_sign PETITION EMAIL
-- Check whether the PETITION is valid for EMAIL to sign.
-- Returns one of:
--      ok          petition is OK to sign
--      none        no such petition exists
--      finished    petition has expired
--      signed      signer has already signed this petition
create function petition_is_valid_to_sign(integer, text)
    returns text as '
    declare
        p record;
    begin
        select into p *
            from petition
            where petition.id = $1;

        if not found then
            return ''none'';
        end if;

        -- check for signed before finished, so repeat sign-ups by same
        -- person give the best message
        if $2 = p.email then
            return ''signed'';
        end if;
        perform signer.id from signer
            where petition_id = $1
                and signer.email = $2;
        if found then
            return ''signed'';
        end if;

        if p.deadline < ms_current_date() then
            return ''finished'';
        end if;
        
        return ''ok'';
    end;
    ' language 'plpgsql';

-- petition_last_change_time PETITION
-- Return the time of the last change to PETITION.
create function petition_last_change_time(integer)
    returns timestamp as '
    declare
        t timestamp;
        t2 timestamp;
    begin
        t := (select creationtime from petition where id = $1);
--        t2 := (select changetime from petition where id = $1);
--        if t2 > t then
--            t = t2;
--        end if;
        t2 := (select signtime from signer where petition_id = $1 order by signtime desc limit 1);
        if t2 > t then
            t = t2;
        end if;
        return t;
    end;
' language 'plpgsql';
