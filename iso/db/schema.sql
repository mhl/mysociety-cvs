-- CREATE FUNCTION plpgsql_call_handler()
--         RETURNS OPAQUE AS '$libdir/plpgsql' LANGUAGE 'C';
-- CREATE TRUSTED PROCEDURAL LANGUAGE 'plpgsql' HANDLER plpgsql_call_handler
--     LANCOMPILER 'PL/pgSQL';

-- Creating geometry_columns and spatial_ref_sys tables and populating them:
-- /usr/share/postgresql-8.3-postgis/lwpostgis.sql
-- /usr/share/postgresql-8.3-postgis/spatial_ref_sys.sql

-- The following must all be done also as the postgres database user,
-- because the geometry_columns can't be modified otherwise.

-- Every station
create table station (
    id serial not null primary key,
    text_id text not null, -- identifier from NPTDR

    connectedness   integer not null,
    minimum_zoom    integer default 0
);
create unique index station_text_id_idx on station(text_id);
create index station_minimum_zoom_idx on station(minimum_zoom);

-- SRID 27700 = OSGB 1936 / British National Grid
select AddGeometryColumn('', 'station', 'position_osgb', 27700, 'POINT', 2);
-- SRID 900913 = Spherical mercator
select AddGeometryColumn('', 'station', 'position_merc', 900913, 'POINT', 2);
create index station_position_merc on station using GIST (position_merc);

-- Represents a map made by the user
create table map (
    id serial not null primary key,
    created timestamp not null default now(),

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

    target_postcode text not null,
    target_easting double precision not null,
    target_northing double precision not null

--  target_station integer not null references station(id)
);


-- SELECT * FROM geotable WHERE ST_DWithin(geocolumn, 'POINT(1000 1000)', 100.0);
-- SELECT road_id, AsText(road_geom) AS geom, road_name FROM roads; 
-- col=# insert into place_time values (1, 39, ST_SetSRID(GeomFromText('POINT(415431 132508)'), 27700));

-- col=# select *, AsText(position), AsText(ST_Transform(position, 4326)) from place_time;
-- col=# select AsText(ST_Transform(ST_SetSRID(GeomFromText('POINT(-1.78103 51.09168)'), 4326) , 27700));
-- http://www.nabble.com/SRID-tranformations-(OSGB-1936)-td20096957.html


