#!/usr/bin/python2.5
#
# i-am-traffic.py: Load tester for Contours of Life.
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: francis@mysociety.org; WWW: http://www.mysociety.org/
#

# Todo: 
# Get CloudMade tiles

import sys
import optparse
import random
import urllib2
import socket
import os
import datetime
import time
import re
import imghdr
import traceback
import threading
import thread

sys.path.extend(("../pylib", "../../pylib", "/home/matthew/lib/python"))

import mysociety.config
import mysociety.mapit
mysociety.config.set_file("../conf/general")

import geoconvert

parser = optparse.OptionParser()

parser.set_usage('''
./i-am-traffic.py [OPTIONS]

Load tests isochrone public transport map generation website by simulating "map
sessions". A "map session" consists of asking for a public transport map for a
random postcode, waiting for it to be made, and downloading 40 isochrone tiles
in the vicinity of the postcode at different zoom levels.
''')

parser.add_option('--top-level-url', type='string', dest="top_level_url", help='website to load tests; defaults to value of BASE_URL from conf/general which is %default', default=mysociety.config.get('BASE_URL'))
parser.add_option('--inter-request-wait', type='float', dest="inter_request_wait", help='within one "map session", how long in seconds to wait between requests to spread them out a bit; default %default', default=0.1)
parser.add_option('--tiles-in-session', type='int', dest="tiles_in_session", help='number of tiles a user gets in one "map session"; default %default', default=40)
parser.add_option('--instances', type='int', dest="instances", help='number of concurrent worker threads that are simulating "map sessions"; default %default', default=1)
parser.add_option('--single-postcode', dest='single_postcode', default=None, help='uses the same postcode for each "map session", rather than the default of a random one each time; use for load testing of cached maps')
parser.add_option('--max-sessions-per-worker', type='int', dest="max_sessions_per_worker", help='if present, terminates when average number of sessions completed by a worker reaches this value; default is to carry on forever', default=None)

(options, args) = parser.parse_args()

# Remove trailing slash if there is one
if options.top_level_url[-1] == '/':
    options.top_level_url = options.top_level_url[0:-1]

#######################################################################################
# Helper functions

# Used at the start of each logfile line
def stamp():
    return threading.currentThread().getName() + " " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Write something to logfile
def log(str):
    print stamp(), str
    sys.stdout.flush()
# Write something to logfile
def verbose(str):
    print stamp(), str
    sys.stdout.flush()

# Display time taken
def format_timedelta(td):
    assert td.days == 0
    return "%d.%06d" % (td.seconds, td.microseconds)
def timedelta_in_secs(td):
    return float(td.days) * (24 * 60 * 60) + float(td.seconds) + (float(td.microseconds) / 1000000)

# Get a random postcode - we go via getting a random westminster constituency.
WMC_areas = mysociety.mapit.get_areas_by_type('WMC')
def get_random_uk_postcode():
    area = random.choice(WMC_areas)
    return mysociety.mapit.get_example_postcode(area)
# Exclude postcodes in Northern Ireland, as NPTDR doesn't cover it
def get_random_gb_postcode():
    while True:
        postcode = get_random_uk_postcode()
        areas_in_postcode = mysociety.mapit.get_voting_areas(postcode)
        if 'NIA' not in areas_in_postcode:
            return postcode

# Return end part of tile URL, randomly from different zoom levels, tiles
# near to the specified lat/lon
# XXX should get differing zoom levels, and get tiles near destination point ideally
def get_random_tile_url_part(lat, lon):
    zoom = random.randint(8, 14)
    (xtile, ytile) = geoconvert.wgs84_to_tile(lat, lon, zoom)
    (xtile, ytile) = (int(xtile), int(ytile))

    xtile += random.randint(-2, 2)
    ytile += random.randint(-2, 2)

    return "/" + str(zoom) + "/" + str(xtile) + "/" + str(ytile) + ".png"

# Primitive WWW::Mechanize type functions
def get_url(path):
    time.sleep(options.inter_request_wait)
    verbose("GET " + path)
    if path[0] == '/':
        full_path = options.top_level_url + path
    else:
        full_path = path
    try:
        return urllib2.urlopen(full_path).read()
    except urllib2.HTTPError, e:
        print "URL: ", e.geturl()
        print "Headers: ", e.info()
        print e.read()
        raise e
def check_content(content, text):
    if text not in content:
        raise Exception("Could not find " + text + " in: " + content)
def re_check_content(content, regexp):
    matches = re.search(regexp, content)
    if not matches:
        raise Exception("Could not find " + regexp + " in: " + content)
    return matches.groups()

#######################################################################################
# Main code to simulate map session

def do_map_session():
    if options.single_postcode:
        postcode = options.single_postcode
    else:
        postcode = get_random_gb_postcode()
    log("new web session with postcode " + postcode)
    loc = mysociety.mapit.get_location(postcode)
    lat, lon = (loc['wgs84_lat'], loc['wgs84_lon'])

    front_page = get_url("/")
    check_content(front_page, "postcode:")

    page = None
    while True:
        page = get_url("/?pc=" + str(postcode))
        if "Showing public transport travel options" in page:
            break
        if "Please provide your email address" in page:
            log("OVERLOADED - server is asking for email address")
        else:
            check_content(page, "automatically refresh")
        log("waiting for route finder")
        time.sleep(2) # HTML refresh number from index.cgi

    iso_tile_url_base = re_check_content(page, """'iso_tile_url_base':\s*'(.*)'""")[0]
    cloudmade_api_key = re_check_content(page, """'cloudmade_api_key':\s*'(.*)'""")[0]
    cloudmade_tile_url_base = "/proxy.cgi?u=http://tile.cloudmade.com/" + cloudmade_api_key + "/998/256"
    log("map iso_tile_url_base: " + iso_tile_url_base + " cloudmade_api_key: " + cloudmade_api_key)

    get_url("/UKTransitTime.swf")
    get_url("/js/swfobject.js")
    get_url("/js/jquery-1.3.2.min.js")
    get_url("/i/header-map.png")
    get_url("/i/logo-c4-small.png")
    get_url("/i/title-small-hover.png")
    get_url("/css.css")
    
    for tile_number in range(0, options.tiles_in_session):
        random_tile_postfix = get_random_tile_url_part(lat, lon)

        iso_tile = get_url(iso_tile_url_base + random_tile_postfix)
        img_type = imghdr.what(None, h=iso_tile)
        if img_type != 'png':
            raise Exception("iso tile not PNG: " + iso_tile)
        log("successfully got iso tile " + str(tile_number + 1) + " of " + str(options.tiles_in_session))

        # Get CloudMade tile - reenable this when it is faster
        #cm_tile = get_url(cloudmade_tile_url_base + random_tile_postfix)
        #img_type = imghdr.what(None, h=cm_tile)
        #if img_type != 'png':
        #    raise Exception("CloudMade file not PNG: " + cm_tile)
        #log("successfully got cloudmade tile " + str(tile_number))

# Run lots of "map sessions"
sessions_completed = 0
sessions_completed_time_taken = datetime.timedelta()
sessions_error = 0
def multiple_map_sessions():
    global sessions_completed, sessions_completed_time_taken, sessions_error

    while True:
        start_time = datetime.datetime.now()
        try:
            do_map_session()
        except (SystemExit, KeyboardInterrupt):
            traceback.print_exc()
            thread.interrupt_main()
        except:
            sessions_error += 1
            log("Error caught")
            traceback.print_exc()
            time.sleep(1)
            continue
        finish_time = datetime.datetime.now()
        time_taken = finish_time - start_time
        sessions_completed += 1
        sessions_completed_time_taken += time_taken
        log("map session took: " + format_timedelta(time_taken) + " secs")

# Make multiple instances
threading.currentThread().setName("progress")
threads = []
for thread_count in range(0, options.instances):
    t = threading.Thread(target=multiple_map_sessions, name="traffic-" + str(thread_count + 1))
    log("threading out " + str(thread_count + 1))
    t.start()
    threads.append(t)

# Parent
while True:
    try:
        # Display progress
        number_of_workers = threading.activeCount() - 1
        assert number_of_workers == len(threads)
        log_message = str(number_of_workers) + " workers"
        if sessions_completed > 0:
            wall_time_per_session = timedelta_in_secs(sessions_completed_time_taken) / sessions_completed
            overall_session_time = wall_time_per_session / float(number_of_workers)
            log_message += ", " + str(round(wall_time_per_session,3)) + " secs/session, " + str(round(overall_session_time,3)) + " secs/concurrent session"
        log_message += " (sessions: %d completed, %d errors)" % (sessions_completed, sessions_error)
        log(log_message)

        # Check for termination
        sessions_per_worker = sessions_completed / number_of_workers
        if options.max_sessions_per_worker and sessions_per_worker >= options.max_sessions_per_worker:
            log("completed " + str(sessions_per_worker) + " sessions per worker")
            log("FINAL: " + log_message)
            break

        # Wait for workers to do stuff before displaying progress again
        time.sleep(5)
    except (SystemExit, KeyboardInterrupt):
        traceback.print_exc()
        # Easiest way to kill all threads on abort
        sys.exit()
            
# Make sure all threads gone
sys.exit()

