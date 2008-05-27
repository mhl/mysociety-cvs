--
-- schema.sql:
-- Schema for user surveys.
--
-- Copyright (c) 2008 UK Citizens Online Democracy. All rights reserved.
-- Email: francis@mysociety.org; WWW: http://www.mysociety.org/
--
-- $Id: schema.sql,v 1.1 2008-05-27 18:56:40 francis Exp $
--

-- secret
-- A random secret.
create table secret (
    secret text not null
);

create table data_item (
    id serial not null primary key,

    user_code text not null,
    site text not null,

    key text not null,
    value text not null,

    whenlogged timestamp not null
);

create index data_item_user_code_idx on data_item(user_code);
create index data_item_site_idx on data_item(site);
create index data_item_key_idx on data_item(key);
create index data_item_value_idx on data_item(value);

create unique index data_item_unique_idx on data_item(user_code, site, key);

