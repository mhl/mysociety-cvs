#!/usr/bin/python
#
# do-nptdr.py:
# Generate diagram of time travel to arrive by a certain time by public
# transport using NPTDR.
#
# Copyright (c) 2008 UK Citizens Online Democracy. All rights reserved.
# Email: francis@mysociety.org; WWW: http://www.mysociety.org/
#

import optparse
import sys
import re
import os
import logging
import datetime
import glob

sys.path.append("../../pylib")
import mysociety.config
import mysociety.mapit

sys.path.append(sys.path[0] + "/../pylib")
import makeplan

mysociety.config.set_file("../conf/general")

parser = optparse.OptionParser()

parser.set_usage('''
Parameters
Can be specified on command line, or in a file passed with --config with each
row of the form "variable: <data>"

Data needs to be in quotes as we don't want shell escaping at that stage.

Examples
--config ../conf/oxford-example
--postcode HP224LY --destination 210021422650 --data "/library/transport/nptdr/sample-bucks/ATCO_040_*.CIF" --size 80000 --px 400 --bandsize 2400 --bandcount 5 --bandcolsep 40 --walkspeed 1 --walktime 3600 --output /home/matthew/public_html/iso
--postcode BS16QF --destination 9100BRSTPWY --data "/library/transport/nptdr/October\ 2008/Timetable\ Data/CIF/Admin_Area_010/*.CIF" --size 200000 --px 800 --bandsize 2400 --bandcount 5 --bandcolsep 40 --walkspeed 1 --walktime 3600 --output /home/matthew/public_html/iso
--postcode OX26DR --destination 340002054WES --data "/library/transport/nptdr/October\ 2008/Timetable\ Data/CIF/Admin_Area_340/*.CIF" --size 10000 --px 800 --bandsize 14 --bandcount 255 --bandcolsep 1 --walkspeed 1 --walktime 3600 --output /home/matthew/public_html/iso
''')

parser.add_option('--postcode', type='string', dest="postcode")
parser.add_option('--destination', type='string', dest="destination")
parser.add_option('--data', type='string', dest="data")
parser.add_option('--size', type='int', dest="size")
parser.add_option('--px', type='int', dest="px")
parser.add_option('--bandsize', type='int', dest="bandsize")
parser.add_option('--bandcount', type='int', dest="bandcount")
parser.add_option('--bandcolsep', type='int', dest="bandcolsep")
parser.add_option('--walkspeed', type='float', dest="walkspeed")
parser.add_option('--walktime', type='int', dest="walktime")
parser.add_option('--endwalkspeed', type='float', dest="endwalkspeed")
parser.add_option('--endwalktime', type='int', dest="endwalktime")
parser.add_option('--config', type='string', dest="config")
parser.add_option('--output', type='string', dest="output")
parser.add_option('--loglevel', type='string', dest="loglevel", default='WARN', help='Try ERROR/WARN/INFO/DEBUG for increasingly more logging, default is WARN.')

(options, args) = parser.parse_args()

if options.config:
    optarr = []
    fp = open(options.config)
    for line in fp:
        (var, val) = re.split("\s*:\s*", line)
        optarr.append("--" + var)
        optarr.append(val.strip())
    fp.close()
    optarr = optarr + sys.argv[1:] # command line args override config
    (options, args) = parser.parse_args(optarr)

#print options; sys.exit()

f = mysociety.mapit.get_location(options.postcode)
N = int(f['northing'])
E = int(f['easting'])

WW = E - options.size / 2;
EE = E + options.size / 2;
SS = N - options.size / 2;
NN = N + options.size / 2;

rect = "%f %f %f %f" % (WW, EE, SS, NN)
outfile = "nptdr-%s-%d" % (options.postcode, options.size)

target_when = datetime.datetime(2008,10,16, 12,0) # Some week in October 2008, need to check exactly when
print logging.getLevelName(options.loglevel)
logging.basicConfig(level=logging.getLevelName(options.loglevel))

# Load in journey tables
nptdr_files = glob.glob(options.data)
atco = makeplan.PlanningATCO()
for nptdr_file in nptdr_files:
    atco.read(nptdr_file)
atco.index_by_short_codes()

#print atco.adjacent_location_times('9100AYLSBRY', datetime.datetime(2007, 10, 9, 9, 0))
#print atco.adjacent_location_times('9100AMERSHM', datetime.datetime(2007, 10, 9, 9, 0))
#atco.find_journeys_crossing_midnight()

# Calculate shortest route from everywhere on network
(results, routes) = atco.do_dijkstra(options.destination, target_when, options.walkspeed, options.walktime)

# Output the results for debugging
grid_time_file = "%s/%s.txt" % (options.output, outfile)
f = open(grid_time_file, "w")
s = "Journey times to " + options.destination + " by " + str(target_when)
f.write("\n")
f.write(s + "\n")
f.write(len(s) * '=\n')
f.write("\n")
for location in sorted(results.keys()):
    when = results[location]

    delta = target_when - when
    mins = delta.seconds / 60 + delta.days * 24 * 60
    f.write(location.ljust(12) + " " + str(mins) + " mins\n")
    route = routes[location]
    route.reverse()
    for waypoint in route:
        f.write("\tleave %s (%s) at %s" % (waypoint.location, atco.location_details[waypoint.location].long_description(), str(waypoint.when)) + "\n")
f.close()

# Output the results for by C grid to contour code
human_file = "%s/%s-human.txt" % (options.output, outfile)
f = open(human_file, "w")
for location, when in results.iteritems():
    delta = target_when - when
    secs = delta.seconds + delta.days * 24 * 60 * 60
    loc = atco.location_details[location]
    f.write(str(loc.additional.grid_reference_easting) + " " + str(loc.additional.grid_reference_northing) + " " + str(secs) + "\n")
f.close()

os.system("cat %s/%s.txt | ./transportdirect-journeys-to-grid grid %s %d %d %f %d > %s/%s-grid" % (options.output, outfile, rect, options.px, options.px, options.endwalktime, options.endwalktime, options.output, outfile))
os.system("cat %s/%s-grid | ./grid-to-ppm field %s %d %d %d %d %d > %s/%s.ppm" % (options.output, outfile, rect, options.px, options.px, options.bandsize, options.bandcount, options.bandcolsep, options.output, outfile))

timestring = time.strftime("%Y-%m-%d-%H:%M:%S")
os.system("convert %s/%s.ppm %s/%s.%s.png" % (options.output, outfile, options.output, outfile, timestring))
print "finished: %s/%s.%s.png" % (options.output, outfile, timestring)
#eog $output/$outfile.png


