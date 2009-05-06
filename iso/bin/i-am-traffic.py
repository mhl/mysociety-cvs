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

sys.path.extend(("../pylib", "../../pylib", "/home/matthew/lib/python"))

import mysociety.config
import mysociety.mapit
mysociety.config.set_file("../conf/general")

import geoconvert

parser = optparse.OptionParser()

parser.set_usage('''
./opt-parse.py [OPTIONS]
''')

parser.add_option('--top-level-url', type='string', dest="top_level_url", help='Defaults to value from conf/general', default=mysociety.config.get('BASE_URL'))
parser.add_option('--inter-request-wait', type='float', dest="inter_request_wait", help='Within one web session, how long in seconds to wait between requests to spread them out a bit.', default=0.1)
parser.add_option('--tiles-in-session', type='int', dest="tiles_in_session", help='Number of tiles a user gets in one web session.', default=40)
parser.add_option('--instances', type='int', dest="instances", help='Number of processes to fork into', default=1)

(options, args) = parser.parse_args()

# Remove trailing slash if there is one
if options.top_level_url[-1] == '/':
    options.top_level_url = options.top_level_url[0:-1]

#######################################################################################
# Helper functions

def server_and_pid():
    return socket.gethostname() + ":" + str(os.getpid())

# Used at the start of each logfile line
def stamp():
    return server_and_pid() + " " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Write something to logfile
def log(str):
    print stamp(), str
    sys.stdout.flush()
# Write something to logfile
def verbose(str):
    print stamp(), str
    sys.stdout.flush()

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
    log("got map iso_tile_url_base: " + iso_tile_url_base + " cloudmade_api_key: " + cloudmade_api_key)

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

# Make multiple instances
for fork_count in range(0, options.instances - 1):
    log("forking time " + str(fork_count + 1))
    pid = os.fork()
    if pid == 0:
        # child
        break

# Run lots of "map sessions"
while True:
    try:
        do_map_session()
    except (SystemExit, KeyboardInterrupt):
        traceback.print_exc()
        break
    except:
        traceback.print_exc()
        time.sleep(1)

