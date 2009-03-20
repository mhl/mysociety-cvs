-- schema.sql:
-- Schema for Contours of Life database.
--
-- Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
-- Email: francis@mysociety.org; WWW: http://www.mysociety.org/
--
-- $Id: schema.sql,v 1.1 2009-03-20 00:35:28 francis Exp $
--

-- A random secret.
create table secret (
    secret text not null
);

-- Represents a map made by the user
create table map (
    id serial not null primary key,
    created timestamp not null default now(),

    -- unique identifier used in URLs - hash of input vars
    url_name text not null, 

    -- workflow 
    state text not null check (
        state = 'new'
        or state = 'generating'
        or state = 'complete'
    ),

    -- Used to show progress while state == 'generating'
    progress_pos integer,
    progress_max integer,
    -- Which server / process is generating it
    progress_server text, 

    -- Parameters used to make the map
    target_mins_after_midnight integer not null,
    target_date date not null, 

    -- Where the map is going to
    target_postcode text not null,
    target_easting double precision not null,
    target_northing double precision not null
);

-- For each map
create table place_time (
    map_id integer not null references map(id),

    minutes_to_target integer not null
);
-- SRID 27700 = OSGB 1936 / British National Grid
select AddGeometryColumn('', 'place_time','position',27700,'POINT',2);
-- create index problem_state_easting_northing_idx on problem(state, easting, northing);
-- CREATE INDEX [indexname] ON [tablename] USING GIST ( [geometrycolumn] );


-- SELECT * FROM geotable WHERE ST_DWithin(geocolumn, 'POINT(1000 1000)', 100.0);
-- SELECT road_id, AsText(road_geom) AS geom, road_name FROM roads; 
-- col=# insert into place_time values (1, 39, ST_SetSRID(GeomFromText('POINT(415431 132508)'), 27700));

-- col=# select *, AsText(position), AsText(ST_Transform(position, 4326)) from place_time;
-- col=# select AsText(ST_Transform(ST_SetSRID(GeomFromText('POINT(-1.78103 51.09168)'), 4326) , 27700));
-- http://www.nabble.com/SRID-tranformations-(OSGB-1936)-td20096957.html





