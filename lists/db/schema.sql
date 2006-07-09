--
-- schema.sql:
-- Schema for simple web mail archive.
--
-- Copyright (c) 2006 UK Citizens Online Democracy. All rights reserved.
-- Email: chris@mysociety.org; WWW: http://www.mysociety.org/
--
-- $Id: schema.sql,v 1.4 2006-07-09 15:20:03 chris Exp $
--

create sequence global_seq;

create table list (
    id integer not null default nextval('global_seq'),
    name text not null
);

create table message (
    id integer not null default nextval('global_seq'),
    -- raw copy of message
    data bytea not null,
    -- various fields extracted from the message
    hdr_message_id text,
    hdr_subject text,
    hdr_from text,
    hdr_to text,
    hdr_cc text,
    hdr_date text,
    hdr_references text,
    hdr_in_reply_to text,
    -- extracted text form, if any
    bodytext text,
    -- best estimate of the time we got the message
    whenreceived timestamptz not null,
);

create unique index message_hdr_message_id_idx on message(hdr_message_id);

create table list_message (
    list_id integer not null references list(id),
    message_id integer not null references message(id)
);

create index list_message_list_id_idx on list_message(list_id);
create index list_message_message_id_idx on list_message(message_id);

