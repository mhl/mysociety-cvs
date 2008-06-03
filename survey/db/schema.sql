--
-- schema.sql:
-- Schema for user surveys.
--
-- Copyright (c) 2008 UK Citizens Online Democracy. All rights reserved.
-- Email: francis@mysociety.org; WWW: http://www.mysociety.org/
--
-- $Id: schema.sql,v 1.2 2008-06-03 19:05:32 francis Exp $
--

-- secret
-- A random secret.
create table secret (
    secret text not null
);

-- Records if the survey has been done
create table survey_done (
    user_code text not null
);
create unique index survey_done_unique_idx on survey_done(user_code);

-- Stores a row for each piece of info in the survey.
create table data_item (
    -- Batch is a random code for the chunk of data.
    batch text not null,
    site text not null,

    key text not null,
    value text not null,

    whenstored date not null
);

create index data_item_batch_idx on data_item(batch);
create index data_item_site_idx on data_item(site);
create index data_item_key_idx on data_item(key);
create index data_item_value_idx on data_item(value);

create unique index data_item_unique_idx on data_item(batch, key);

