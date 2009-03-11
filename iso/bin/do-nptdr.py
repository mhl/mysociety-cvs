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
import glob
import datetime
import time
import mx.DateTime
try: 
    import cProfile
except:
    pass
import pstats

sys.path.append("../../pylib")
import mysociety.config
import mysociety.mapit

sys.path.append(sys.path[0] + "/../pylib")
import makeplan
import fastplan

mysociety.config.set_file("../conf/general")

parser = optparse.OptionParser()

parser.set_usage('''
./do-nptdr.py [PARAMETERS] [COMMAND]

Generate a contour map showing how long it takes to get somewhere in the UK by
public transport. Reads ATCO-CIF timetable files. Outputs a PNG file.

Commands:
    plan - create map 
    stats - dump statistics about files
    midnight - output journeys that cross midnight
    fast - output fast data structure for C++ code
    fastplan - as fast, but also calls out to the quick planning C++ code
Default is to run "plan".

Parameters:
Can be specified on command line, or in a file passed with --config with each
row of the form "variable: <data>"

Examples
--config ../conf/oxford-example
--postcode HP224LY --destination 210021422650 --data "/library/transport/nptdr/sample-bucks/ATCO_040_*.CIF" --size 80000 --px 400 --bandsize 2400 --bandcount 5 --bandcolsep 40 --walkspeed 1 --walktime 3600 --output /home/matthew/public_html/iso
--postcode BS16QF --destination 9100BRSTPWY --data "/library/transport/nptdr/October\ 2008/Timetable\ Data/CIF/Admin_Area_010/*.CIF" --size 200000 --px 800 --bandsize 2400 --bandcount 5 --bandcolsep 40 --walkspeed 1 --walktime 3600 --output /home/matthew/public_html/iso
--postcode OX26DR --destination 340002054WES --data "/library/transport/nptdr/October\ 2008/Timetable\ Data/CIF/Admin_Area_340/*.CIF" --size 10000 --px 800 --bandsize 14 --bandcount 255 --bandcolsep 1 --walkspeed 1 --walktime 3600 --output /home/matthew/public_html/iso
''')

parser.add_option('--destination', type='string', dest="destination", help='Target location for route finding, as in ATCO-CIF file e.g. 9100MARYLBN')
parser.add_option('--whenarrive', type='string', dest="whenarrive", help='Time and date to arrive at destination by. Must be a day for which the ATCO-CIF timetables loaded are valid. Fairly freeform format, e.g. "15 Oct 2008, 9:00"', default="15 Oct 2008, 9:00") # Some week in October 2008, need to check exactly when
parser.add_option('--data', type='string', dest="data", help='ATCO-CIF files containing timetables to use. At the command line, put the value in quotes, file globs such as * will be expanded later.')
parser.add_option('--hours', type='float', dest="hours", help='Longest journey length, in hours. Route finding algorithm will stop here.', default=1)
parser.add_option('--postcode', type='string', dest="postcode", help='Location of centre of map')
parser.add_option('--size', type='int', dest="size", help='Sides of map rectangle in metres, try 10000')
parser.add_option('--px', type='int', dest="px", help='Sides of output contour image file in pixels', default=800)
parser.add_option('--bandsize', type='int', dest="bandsize", help='Journey time in seconds that each contour band of image file represents', default=600)
parser.add_option('--bandcount', type='int', dest="bandcount", help='Number of contour bands to have in total', default=200)
parser.add_option('--bandcolsep', type='int', dest="bandcolsep", help='Number of shades between each contour band (starts at RGB 255/255/255, goes down through shades of grey with this step)', default=1)
parser.add_option('--walkspeed', type='float', dest="walkspeed", help='Speed to walk between nearby stations at interchanges mid-journey in m/s', default=1)
parser.add_option('--walktime', type='int', dest="walktime", help='Maximum time in seconds to walk for interchanges', default=300)
parser.add_option('--endwalkspeed', type='float', dest="endwalkspeed", help='Speed to walk to first stop at beginning of journey in m/s', default=1)
parser.add_option('--endwalktime', type='float', dest="endwalktime", help='Maximum time in seconds to walk to first stop of journey', default=900)
parser.add_option('--config', type='string', dest="config", help='Specify a text file containing parameters to load. Format is a parameter per line, value coming after a colon, e.g. "bandsize: 14". Command line parameters override the config file.' )
parser.add_option('--output', type='string', dest="output", help='Output directory.')
parser.add_option('--loglevel', type='string', dest="loglevel", default='WARN', help='Try ERROR/WARN/INFO/DEBUG for increasingly more logging, default is WARN.')
parser.add_option('--profile', action='store_true', dest='profile', default=False, help="Runs Python profiler on Dijkstra's algorithm part of calculation. Outputs a .profile file in output directory for later processing by Python pstats module, and prints basic details from it.")
parser.add_option('--viewer', type='string', dest="viewer", help='If present, calls application to display PNG file at end.')

(options, args) = parser.parse_args()

if options.config:
    optarr = []
    fp = open(options.config)
    for line in fp:
        (var, val) = re.split("\s*:\s*", line, maxsplit=1)
        optarr.append("--" + var)
        optarr.append(val.strip())
    fp.close()
    optarr = optarr + sys.argv[1:] # command line args override config
    (options, args) = parser.parse_args(optarr)

if not options.postcode:
    raise Exception, 'Must supply some data!'
if len(args) > 1:
    raise Exception, 'Give at most one command'
if len(args) == 0:
    args = ['plan']
command = args[0]
if command not in ['plan', 'stats', 'midnight', 'fast', 'fastplan']:
    raise Exception, 'Unknown command'

f = mysociety.mapit.get_location(options.postcode)
N = int(f['northing'])
E = int(f['easting'])

WW = E - options.size / 2;
EE = E + options.size / 2;
SS = N - options.size / 2;
NN = N + options.size / 2;

rect = "%f %f %f %f" % (WW, EE, SS, NN)
outfile = "nptdr-%s-%d" % (options.postcode, options.size)

target_when = datetime.datetime.fromtimestamp(mx.DateTime.DateTimeFrom(options.whenarrive))
scan_back_when = target_when - datetime.timedelta(hours=options.hours)

logging.basicConfig(level=logging.getLevelName(options.loglevel))

nptdr_files = glob.glob(options.data)

# Run external command, and log what did
def run_cmd(cmd):
    logging.info("external command: " + cmd)
    os.system(cmd)

# Calls Chris Lightfoot's old C code to make contour files
def do_external_contours():
    run_cmd("cat %s/%s.txt | ./transportdirect-journeys-to-grid grid %s %d %f %f %d > %s/%s-grid" % (options.output, outfile, rect, options.px, options.px, options.endwalkspeed, options.endwalktime, options.output, outfile))
    run_cmd("cat %s/%s-grid | ./grid-to-ppm field %s %d %d %d %d %d > %s/%s.ppm" % (options.output, outfile, rect, options.px, options.px, options.bandsize, options.bandcount, options.bandcolsep, options.output, outfile))

    timestring = time.strftime("%Y-%m-%d-%H.%M.%S")
    run_cmd("convert %s/%s.ppm %s/%s.%s.png" % (options.output, outfile, options.output, outfile, timestring))

    print "finished: %s/%s.%s.png" % (options.output, outfile, timestring)

    if options.viewer:
        run_cmd(options.viewer + " %s/%s.%s.png" % (options.output, outfile, timestring))
#eog $output/$outfile.png


# Handle generating indices for C++ version
if command == 'fast' or command == 'fastplan':
    fastindex = "%s/%s.fastindex" % (options.output, outfile)
    atco = fastplan.FastPregenATCO(fastindex, nptdr_files, target_when.date())
    if command == 'fastplan':
        run_cmd("../pylib/makeplan %s/%s %d %s" % (options.output, outfile, target_when.hour * 60 + target_when.minute, options.destination))
        outfile = outfile + ".fast"
        do_external_contours()
    sys.exit()

# Load in journey tables
atco = makeplan.PlanningATCO()
for nptdr_file in nptdr_files:
    atco.read(nptdr_file)

# Handle midnight command
if command == 'midnight':
    atco.print_journeys_crossing_midnight()
    sys.exit()

# Stuff that we only run once for multiple maps. Note that we don't want to
# profile it - we are optimising for map making once we've got going, not
# precomputing indices.
atco.precompute_for_dijkstra(walk_speed=options.walkspeed, walk_time=options.walktime)

# Handle statistics command
if command == 'stats':
    print atco.statistics()
    sys.exit()

# Otherwise we're at the planning command

# Calculate shortest route from everywhere on network
def profile_me():
    return atco.do_dijkstra(options.destination, target_when, walk_speed=options.walkspeed, walk_time=options.walktime, earliest_departure=scan_back_when)
if options.profile:
    profile_file = "%s/%s.profile" % (options.output, outfile)
    cProfile.run("(results, routes) = profile_me()", profile_file)
    p = pstats.Stats(profile_file)
    p.strip_dirs().sort_stats(-1).print_stats()
else:
    (results, routes) = profile_me()

# Output the results for by C grid to contour code
grid_time_file = "%s/%s.txt" % (options.output, outfile)
f = open(grid_time_file, "w")
for location, when in results.iteritems():
    delta = target_when - when
    secs = delta.seconds + delta.days * 24 * 60 * 60
    loc = atco.location_from_id[location]
    f.write(str(loc.additional.grid_reference_easting) + " " + str(loc.additional.grid_reference_northing) + " " + str(secs) + "\n")
f.close()

# Output the results for debugging
human_file = "%s/%s-human.txt" % (options.output, outfile)
f = open(human_file, "w")
s = "Journey times to " + options.destination + " by " + str(target_when)
f.write("\n")
f.write(s + "\n")
f.write(len(s) * '=' + '\n')
f.write("\n")
f.write(atco.pretty_print_routes(routes))
f.close()

do_external_contours()


