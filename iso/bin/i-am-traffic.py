#!/usr/bin/python2.5
#
# i-am-traffic.py: Load tester for Contours of Life.
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: francis@mysociety.org; WWW: http://www.mysociety.org/
#

# Todo: 
# Check what happens on error cases
# Get CSS files
# Get CloudMade tiles
# Improve range of random tile get
# Check tile got is PNG

import sys
import optparse
import random
import urllib
import socket
import os
import datetime
import time
import re
import imghdr

sys.path.extend(("../pylib", "../../pylib", "/home/matthew/lib/python"))

import mysociety.config
import mysociety.mapit
mysociety.config.set_file("../conf/general")


parser = optparse.OptionParser()

parser.set_usage('''
./opt-parse.py [OPTIONS]
''')

parser.add_option('--top-level-url', type='string', dest="top_level_url", help='Without the terminating slash, please.', default='http://col.cat')
parser.add_option('--inter-request-wait', type='float', dest="inter_request_wait", help='Within one web session, how long in seconds to wait between requests to spread them out a bit.', default=0.1)
parser.add_option('--tiles-in-session', type='int', dest="tiles_in_session", help='Number of tiles a user gets in one web session.', default=40)
parser.add_option('--instances', type='int', dest="instances", help='Number of processes to fork into', default=1)

(options, args) = parser.parse_args()

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

# Return end part of tile URL, randomly from country
# XXX should get differing zoom levels, and get tiles near destination point ideally
def get_random_tile_url_part():
    return "/11/" + str(random.randint(700, 1300)) + "/" + str(random.randint(300, 700)) + ".png"

# Primitive WWW::Mechanize type functions
def get_url(path):
    time.sleep(options.inter_request_wait)
    verbose("GET " + path)
    if path[0] == '/':
        full_path = options.top_level_url + path
    else:
        full_path = path
    return urllib.urlopen(full_path).read()
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

    front_page = get_url("/")
    check_content(front_page, "postcode:")

    page = None
    while True:
        page = get_url("/?pc=" + str(postcode))
        if "Your map will load below" in page:
            break
        check_content(page, "automatically refresh")
        log("waiting for route finder")
        time.sleep(2) # HTML refresh number from index.cgi

    iso_tile_url_base = re_check_content(page, """'iso_tile_url_base':\s*'(.*)'""")[0]
    cloudmade_api_key = re_check_content(page, """'cloudmade_api_key':\s*'(.*)'""")[0]
    log("got map iso_tile_url_base: " + iso_tile_url_base + " cloudmade_api_key: " + cloudmade_api_key)

    get_url("/UKTransitTime.swf")
    
    for tile_number in range(0, options.tiles_in_session):
        random_tile_postfix = get_random_tile_url_part()
        tile = get_url(iso_tile_url_base + random_tile_postfix)
        img_type = imghdr.what(None, h=tile)
        if img_type != 'png':
            raise Exception("Not PNG file: " + tile)
        log("successfully got tile " + str(tile_number))

# Make multiple instances
for fork_count in range(0, options.instances - 1):
    log("forking time " + str(fork_count))
    pid = os.fork()
    if pid == 0:
        # child
        break

# Run lots of "map sessions"
while True:
    do_map_session()

