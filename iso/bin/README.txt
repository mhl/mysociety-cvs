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

Transport direct specific
=========================

transportdirect-scrape - screen scrapes transport direct to make file of
        journey times from public transport stops to arrive by certain time on 
        certain day.
transportdirect-journeys-to-grid - takes journey times from public transport
        stops and generates a grid of journey times by adding on walking times
        from home to the public transport stops.
grid-to-ppm - converts grid into displayable image
do-transportdirect - runs transportdirect scraper and makes final PNG image

House price specific
====================

landregistry-to-houseprice - convert CSV file from land registry into "E N date price" file
houseprice-inflate - inflate a set of house prices to the last month in the data set, using
        median values in each month to work out inflation rate.
houseprice-mask - convert "E N date price" file into a bitmap mask according to a threshold
do-houses - runs all scripts in house price mask generator and makes final PNG

Not yet used/ready/named properly
=================================

map-from-cycle.c - XXX

