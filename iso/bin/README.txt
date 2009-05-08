These scripts generate isochrone maps of transport distances to locations, and
house price maps, and other similar goodies. 

See "Travel-time Maps and their Uses", the first report made using these scripts
(or their ancestors, anyway), for an overview:
    http://www.mysociety.org/2006/travel-time-maps/

README-check - check this file is up to date

General loading scripts
=======================

postcodes-into-db - loads postcodes from OS's CodePoint into an SQLite database
stops-into-db - loads NaPTAN stops into an SQLite database
calc-bounding-rectangle - given a postcode and size gives you the OS grid bounding rectangle

Public transport specific
=========================

transportdirect-scrape - screen scrapes transport direct to make file of
        journey times from public transport stops to arrive by certain time on 
        certain day.
tfl-scrape - similar, but uses Transport for London's journey planner (London
        only, but allegedly quicker)
transportdirect-journeys-to-grid - takes journey times from public transport
        stops and generates a grid of journey times by adding on walking times
        from home to the public transport stops.
grid-to-ppm - converts grid into displayable image
do-transportdirect - runs transportdirect scraper and makes final PNG image
do-tfl - runs tfl scraper and makes final PNG image

House price specific
====================

landregistry-to-houseprice - convert CSV file from land registry into "E N date price" file
houseprice-inflate - inflate a set of house prices to the last month in the data set, using
        median values in each month to work out inflation rate.
houseprice-mask - convert "E N date price" file into a bitmap mask according to a threshold
do-houses - runs all scripts in house price mask generator and makes final PNG

Cambridge cycling map
=====================

do-camcycle - never really finished/used, but useful if you have lat/lon coords in UK
calc-bounding-rectangle-latlon - goes from UK postcode to lat/lon bounding rectangle 

European train maps
===================

Old scrapers 
------------

dbbahn-stations-scrape - get list of European rail stations from bahn.de
euro-stations-location - use Google Maps to find the location of stations by name
dbbahn-timings-scrape - grab HTML pages of route queries for a list of stations
dbbahn-timings-parse - parses HTML pages to get journey durations
euro-merge-located-duration - script to merge together the above

Newer simpler scrapers
----------------------

euro-geonames-grid-dbbhan-scrape - takes city names from geonames, and feeds into bahn.de
euro-tsv-to-located-duration - converts output of above into input for do-eurotrain below

Map renderer
------------

eurotrain-journeys-to-grid - mercator projection lat/lon map making C code
do-eurotrain - script that makes the maps for the European trains

Contours of Life
================

do-nptdr.py - script to call Python journey planner and make map
fastplan.cpp - C++ journey planner
fastplan-coopt.cpp - coopeted C++ journey planner, for calling by isodaemon
isodaemon.py - daemon to call C++ planner and make .iso route files

post-deploy-setup - used when deploying the site
generate-config - used when deploying the site
make-logos.php - generate Mapumental logos
test-run - test script for Contours of Life

clear-generated-maps - erase maps entries in database and .iso route files
clear-tile-cache - clear tile server's cache of tiles

populate-all - generate binary files for C++ journey planner, and put stations in database
cull_stations.py - calculate render threshold for stations at different zoom levels

i-am-traffic.py - load test Contours of Life
traffic-analyse - run i-am-traffic.py with varying numbers of worker map sessions

do-westmidlands-anim - on off to make an animation

Not yet used/ready/named properly
=================================

map-from-cycle.c - XXX

est-run
