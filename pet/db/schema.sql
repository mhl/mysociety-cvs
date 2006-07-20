-- schema.sql:
-- Schema for petitions database.
--
-- Copyright (c) 2006 UK Citizens Online Democracy. All rights reserved.
-- Email: francis@mysociety.org; WWW: http://www.mysociety.org/
--
-- $Id: schema.sql,v 1.9 2006-07-20 13:20:05 matthew Exp $
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

-- users, but call the table person rather than user so we don't have to quote
-- its name in every statement....
create table person (
    id integer not null primary key default nextval('global_seq'),
    name text,
    email text not null,
    password text,
    website text,
    numlogins integer not null default 0
);

create unique index person_email_idx on person(email);

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
    person_id integer not null references person(id),
    name text not null,
    organisation text not null,
    address text not null,
    postcode text not null,
    telephone text not null,
    org_url text not null,

    -- metadata
    creationtime timestamp not null,
    
    status text not null default 'draft' check (
        status = 'draft' -- petition is waiting for approval
        or status = 'rejectedonce' -- petition has been rejected once
        or status = 'resubmitted' -- petition has been resubmitted
        or status = 'rejected' -- petition has been rejected again, or timed out of rejectedonce
        or status = 'live' -- petition is active
        or status = 'finished' -- deadline has been passed
    ),
    laststatuschange timestamp not null
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
    name text not null,
    address text not null,
    postcode text not null,
    person_id integer references person(id),

    -- whether this signer is included in the petition or not
    showname boolean not null default false,
      
    -- when they signed
    signtime timestamp not null
);

create index signer_petition_id_idx on signer(petition_id);

-- Stores randomly generated tokens and serialised hash arrays associated
-- with them.
create table token (
    scope text not null,        -- what bit of code is using this token
    token text not null,
    data bytea not null,
    created timestamp not null,
    primary key (scope, token)
);

create table requeststash (
    key varchar(16) not null primary key check (length(key) = 8 or length(key) = 16),
    whensaved timestamp not null default ms_current_timestamp(),
    method text not null default 'GET' check (
            method = 'GET' or method = 'POST'
        ),
    url text not null,
    -- contents of POSTed form
    post_data bytea check (
            (post_data is null and method = 'GET') or
            (post_data is not null and method = 'POST')
        ),
    extra text
);

-- petition_is_valid_to_sign PLEDGE EMAIL
-- Whether the given PLEDGE is valid for EMAIL to sign.
-- Returns one of:
--      ok          petition is OK to sign
--      none        no such petition exists
--      finished    petition has expired
--      signed      signer has already signed this petition
create function petition_is_valid_to_sign(integer, text)
    returns text as '
    declare
        p record;
        creator_email text;
    begin
        select into p *
            from petition
            where petition.id = $1 
            for update;
        select into creator_email email
            from person
            where person.id = p.person_id;

        if not found then
            return ''none'';
        end if;

        -- check for signed by email (before finished, so repeat sign-ups
        -- by same person give the best message)
        if $2 is not null then
            if $2 = creator_email then
                return ''signed'';
            end if;
            perform signer.id from signer, person
                where petition_id = $1
                    and signer.person_id = person.id
                    and person.email = $2 for update;
            if found then
                return ''signed'';
            end if;
        end if;

        if p.deadline < ms_current_date() then
            return ''finished'';
        end if;
        
        return ''ok'';
    end;
    ' language 'plpgsql';
