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
import md5

sys.path.append("../../pylib")
import mysociety.config
import mysociety.mapit

sys.path.append(sys.path[0] + "/../pylib")
import makeplan
import fastplan

mysociety.config.set_file("../conf/general")

###############################################################################
# Read parameters

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
--postcode HP224LY --destination 210021422650 --data "/library/transport/nptdr/sample-bucks/ATCO_040_*.CIF" --size 80000 --px 400 --bandsize 2400 --bandcount 5 --bandcolsep 40 --walk_speed 1 --walk_time 3600 --output /home/matthew/public_html/iso
--postcode BS16QF --destination 9100BRSTPWY --data "/library/transport/nptdr/October\ 2008/Timetable\ Data/CIF/Admin_Area_010/*.CIF" --size 200000 --px 800 --bandsize 2400 --bandcount 5 --bandcolsep 40 --walk_speed 1 --walk_time 3600 --output /home/matthew/public_html/iso
--postcode OX26DR --destination 340002054WES --data "/library/transport/nptdr/October\ 2008/Timetable\ Data/CIF/Admin_Area_340/*.CIF" --size 10000 --px 800 --bandsize 14 --bandcount 255 --bandcolsep 1 --walk_speed 1 --walk_time 3600 --output /home/matthew/public_html/iso
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
parser.add_option('--walkspeed', type='float', dest="walk_speed", help='Speed to walk between nearby stations at interchanges mid-journey in m/s', default=1)
parser.add_option('--walktime', type='int', dest="walk_time", help='Maximum time in seconds to walk for interchanges', default=300)
parser.add_option('--endwalkspeed', type='float', dest="endwalk_speed", help='Speed to walk to first stop at beginning of journey in m/s', default=1)
parser.add_option('--endwalktime', type='float', dest="endwalk_time", help='Maximum time in seconds to walk to first stop of journey', default=900)
parser.add_option('--config', type='string', dest="config", help='Specify a text file containing parameters to load. Format is a parameter per line, value coming after a colon, e.g. "bandsize: 14". Command line parameters override the config file.' )
parser.add_option('--output', type='string', dest="output", help='Output directory.')
parser.add_option('--loglevel', type='string', dest="loglevel", default='WARN', help='Try ERROR/WARN/INFO/DEBUG for increasingly more logging, default is WARN.')
parser.add_option('--profile', action='store_true', dest='profile', default=False, help="Runs Python profiler on Dijkstra's algorithm part of calculation. Outputs a .profile file in output directory for later processing by Python pstats module, and prints basic details from it.")
parser.add_option('--viewer', type='string', dest="viewer", help='If present, calls application to display PNG file at end.')

(options, args) = parser.parse_args()

# Merge in options from file
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

# Work out command
if len(args) > 1:
    raise Exception, 'Give at most one command'
if len(args) == 0:
    args = ['plan']
command = args[0]
if command not in ['plan', 'stats', 'midnight', 'fastcalc', 'fastplan']:
    raise Exception, 'Unknown command'

# Required parameters
nptdr_files = glob.glob(options.data)

# Parameters used by do_external_contours
if command in ['plan', 'fastplan']:
    f = mysociety.mapit.get_location(options.postcode)
    N = int(f['northing'])
    E = int(f['easting'])

    WW = E - options.size / 2;
    EE = E + options.size / 2;
    SS = N - options.size / 2;
    NN = N + options.size / 2;

    rect = "%f %f %f %f" % (WW, EE, SS, NN)

if command in ['plan', 'fastcalc', 'fastplan']:
    target_when = datetime.datetime.fromtimestamp(mx.DateTime.DateTimeFrom(options.whenarrive))
    scan_back_when = target_when - datetime.timedelta(hours=options.hours)

# Output files
if command in ['plan']:
    outfile = options.output + "/nptdr-slow-%s-%d" % (options.destination, options.size)
if command in ['fastcalc', 'fastplan']:
    outfile = options.output + "/nptdr-fast-%s-%d" % (options.destination, options.size)
    # make a name for index files that depends on their values
    nptdr_files_hash = md5.new(",".join(nptdr_files)).hexdigest()[0:12]
    fastindexfile = options.output + "/fastindex-%s-%s" % (nptdr_files_hash, target_when.date().strftime("%Y-%m-%d"))

if options.profile:
    import cProfile
    import pstats

logging.basicConfig(level=logging.getLevelName(options.loglevel))

###############################################################################
# Helper functions

# Run external command, and log what did
def run_cmd(cmd):
    logging.info("external command: " + cmd)
    ret = os.system(cmd)
    if ret != 0:
        raise Exception("Error code from command: " + cmd)

# Calls Chris Lightfoot's old C code to make contour files
def do_external_contours():
    run_cmd("cat %s.txt | ./transportdirect-journeys-to-grid grid %s %d %f %f %d > %s-grid" % (outfile, rect, options.px, options.px, options.endwalk_speed, options.endwalk_time, outfile))
    run_cmd("cat %s-grid | ./grid-to-ppm field %s %d %d %d %d %d > %s.ppm" % (outfile, rect, options.px, options.px, options.bandsize, options.bandcount, options.bandcolsep, outfile))

    timestring = time.strftime("%Y-%m-%d-%H.%M.%S")
    run_cmd("convert %s.ppm %s.%s.png" % (outfile, outfile, timestring))

    print "finished: %s.%s.png" % (outfile, timestring)

    if options.viewer:
        run_cmd(options.viewer + " %s.%s.png" % (outfile, timestring))

###############################################################################
# Commands

# Show journeys crossing midnight
def midnight():
    atco = makeplan.PlanningATCO()
    atco.read_files(nptdr_files)
    atco.print_journeys_crossing_midnight()

# Show information about the files
def statistics():
    atco = makeplan.PlanningATCO()
    atco.read_files(nptdr_files)
    atco.precompute_for_dijkstra(walk_speed=options.walk_speed, walk_time=options.walk_time)
    print atco.statistics()

# Run Dijkstra's algorithm in Python
def python_plan():
    # Load in journey tables
    atco = makeplan.PlanningATCO()
    atco.read_files(nptdr_files)

    # Stuff that we only run once for multiple maps. Note that we don't want to
    # profile it - we are optimising for map making once we've got going, not
    # precomputing indices.
    atco.precompute_for_dijkstra(walk_speed=options.walk_speed, walk_time=options.walk_time)

    # Calculate shortest route from everywhere on network
    def profile_me():
        return atco.do_dijkstra(options.destination, target_when, walk_speed=options.walk_speed, walk_time=options.walk_time, earliest_departure=scan_back_when)
    if options.profile:
        profile_file = "%s.profile" % outfile
        cProfile.run("(results, routes) = profile_me()", profile_file)
        p = pstats.Stats(profile_file)
        p.strip_dirs().sort_stats(-1).print_stats()
    else:
        (results, routes) = profile_me()

    # Output the results for by C grid to contour code
    grid_time_file = "%s.txt" % outfile
    f = open(grid_time_file, "w")
    for location, when in results.iteritems():
        delta = target_when - when
        secs = delta.seconds + delta.days * 24 * 60 * 60
        loc = atco.location_from_id[location]
        f.write(str(loc.additional.grid_reference_easting) + " " + str(loc.additional.grid_reference_northing) + " " + str(secs) + "\n")
    f.close()

    # Output the results for debugging
    human_file = "%s-human.txt" % outfile
    f = open(human_file, "w")
    s = "Journey times to " + options.destination + " by " + str(target_when)
    f.write("\n")
    f.write(s + "\n")
    f.write(len(s) * '=' + '\n')
    f.write("\n")
    f.write(atco.pretty_print_routes(routes))
    f.close()

    do_external_contours()

# Precalculate binary data files, for later use by faster C++ Dijkstra's algorithm
def fast_calc():
    atco = fastplan.FastPregenATCO(fastindexfile, nptdr_files, target_when.date())

# Call out to C++ version of Dijkstra's algorithm
def fast_plan():
    run_cmd("../pylib/makeplan %s %s %d %s" % (fastindexfile, outfile, target_when.hour * 60 + target_when.minute, options.destination))
    do_external_contours()

###############################################################################
# Main code

if command == 'fastcalc':
    fast_calc()
elif command == 'fastplan':
    fast_plan()
elif command == 'midnight':
    midnight()
elif command == 'stats':
    statistics()
elif command == 'plan':
    python_plan()
   

