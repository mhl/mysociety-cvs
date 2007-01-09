--
-- schema.sql:
-- Description of donors to UKCOD.
--
-- Copyright (c) 2006 UK Citizens Online Democracy. All rights reserved.
-- Email: louise@mysociety.org; WWW: http://www.mysociety.org/
--
-- $Id: schema.sql,v 1.1 2007-01-09 15:44:45 louise Exp $
--

-- donor
--
--
create table donor (
    id serial not null primary key,
    title text not null, 
    firstname text not null,
    surname text not null, 
    address1 text not null,
    address2 text, 
    town text not null, 
    county text,
    postcode text not null,
    country text not null, 
    giftaid boolean not null default false
);

-- secret
-- A random secret.
create table secret (
    secret text not null
);
