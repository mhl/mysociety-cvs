-- schema.sql:
-- Schema for Contours of Life database.
--
-- Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
-- Email: francis@mysociety.org; WWW: http://www.mysociety.org/
--
-- $Id: schema.sql,v 1.32 2009-05-15 14:23:32 matthew Exp $
--

-- The following must be done first to set up PostGIS, as user "postgres":

-- CREATE FUNCTION plpgsql_call_handler()
--         RETURNS OPAQUE AS '$libdir/plpgsql' LANGUAGE 'C';
-- CREATE TRUSTED PROCEDURAL LANGUAGE 'plpgsql' HANDLER plpgsql_call_handler
--     LANCOMPILER 'PL/pgSQL';

-- Creating geometry_columns and spatial_ref_sys tables and populating them:
-- PSQL-SCHEMA-COMPARE-INCLUDE: /usr/share/postgresql-8.3-postgis/lwpostgis.sql
-- PSQL-SCHEMA-COMPARE-INCLUDE: /usr/share/postgresql-8.3-postgis/spatial_ref_sys.sql

-- The following must all be done also as the "postgres" database user,
-- because the geometry_columns can't be modified otherwise.

-- Every station
create table station (
    id integer not null primary key,
    text_id text not null, -- identifier from NPTDR
    long_description text, -- should be NOT NULL later

    connectedness   integer,
    minimum_zoom    integer default 0
);
create unique index station_text_id_idx on station(text_id);
create index station_minimum_zoom_idx on station(minimum_zoom);
create index station_connectedness_idx on station(connectedness);
-- SRID 27700 = OSGB 1936 / British National Grid
select AddGeometryColumn('', 'station', 'position_osgb', 27700, 'POINT', 2) into temp result_add_position_osgb;
-- SRID 900913 = Spherical mercator
select AddGeometryColumn('', 'station', 'position_merc', 900913, 'POINT', 2) into temp result_add_position_merc;
-- (the "into temp" stuff above serves to suppress the output of the return value of the "select AddGeometryColumn")
create index station_position_merc on station using GIST (position_merc);

-- Every journey
create table journey (
    id integer not null primary key,
    text_id text not null, -- identifier from NPTDR
    vehicle_code char(1) -- T for train etc.
);

-- Represents a map made by the user
create table map (
    id serial not null primary key,
    created timestamp not null default now(),

    -- workflow 
    state text not null check (
        state = 'new'
        or state = 'working'
        or state = 'complete'
        or state = 'error'
    ),
    working_server text, -- which isodaemon machine/pid is working / worked on it
    working_start timestamp, -- when an isodaemon started working on it
    working_took float, -- wall clock time for route finding part in seconds

    -- Parameters used to make the map
    target_station_id integer references station(id),
    target_postcode text,
    target_e integer,
    target_n integer,
    target_direction text not null check ( target_direction = 'arrive_by' or target_direction = 'depart_after' ),
    target_time integer not null, -- mins after midnight to arrive by / depart after
    target_limit_time integer not null, -- mins after midnight to go back to / forward to
    target_date date not null,

    check ( (target_direction = 'arrive_by' and target_limit_time <= target_time)
          or (target_direction = 'depart_after' and target_limit_time >= target_time) )
);
create unique index map_unique_station_idx on map(target_station_id, target_direction, target_time, target_limit_time, target_date);
create unique index map_unique_coord_idx on map(target_e, target_n, target_direction, target_time, target_limit_time, target_date);

create table email_queue (
    id serial not null primary key,
    email text not null,
    sent boolean not null default 'f',
    map_id integer not null references map(id)
);

-- House prices
create table house_price (
    id serial not null primary key,
    transaction_date date not null,
    amount integer not null,
    type_of_house char(1) not null, -- D, T, S, F for detached/semi/terrace/flat
    new_build boolean not null,
    tenure char(1) not null, -- F or L for freehold/leasehold
    address text not null
);
-- SRID 27700 = OSGB 1936 / British National Grid
select AddGeometryColumn('', 'house_price', 'position_osgb', 27700, 'POINT', 2) into temp result_add_position_osgb_2;
select AddGeometryColumn('', 'house_price', 'position_merc', 900913, 'POINT', 2) into temp result_add_position_merc_2;
create index house_price_position_merc on house_price using GIST (position_merc);

-- Scenicness
create table scenic (
    id serial not null primary key,
    rating float not null
);
-- SRID 27700 = OSGB 1936 / British National Grid
select AddGeometryColumn('', 'scenic', 'position_osgb', 27700, 'POINT', 2) into temp result_add_position_osgb_3;
select AddGeometryColumn('', 'scenic', 'position_merc', 900913, 'POINT', 2) into temp result_add_position_merc_3;
create index scenic_position_merc on scenic using GIST (position_merc);

-- For invites
create table invite (
    id serial not null primary key,
    email text not null,
    source text not null,
    source_id integer,
    token text,
    num_invites integer not null default 0,
    num_maps integer not null default 3,
    created timestamp not null default now()
);
create unique index invite_token_idx on invite(token);
create unique index invite_email_idx on invite(email);

create table invite_postcode (
    id serial not null primary key,
    invite_id integer not null references invite(id),
    created timestamp not null default now(),
    postcode text not null
);

-- We grant privileges back to the actual user who is using the database.
-- Shame it had to all be made by user "postgres", see top of file.
grant all on table station to col;
grant all on table journey to col;
grant all on table map to col;
grant all on table map_id_seq to col;
grant all on table spatial_ref_sys to col;
grant all on table geometry_columns to col;
grant all on table email_queue to col;
grant all on table email_queue_id_seq to col;
grant all on table house_price to col;
grant all on table house_price_id_seq to col;
grant all on table scenic to col;
grant all on table scenic_id_seq to col;
grant all on table invite to col;
grant all on table invite_id_seq to col;
grant all on table invite_postcode to col;
grant all on table invite_postcode_id_seq to col;

