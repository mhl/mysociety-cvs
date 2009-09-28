#
# isoweb.py:
# Functions for looking up times of public transport routes in .iso files etc.
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: francis@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: isoweb.py,v 1.3 2009-09-28 14:04:32 duncan Exp $

# Default values for various parameters to route finder. These are used when
# not specified in URL (so changing them will change the meaning of old URLs).
default_target_direction = 'arrive_by'
default_target_time = 540 # 09:00
default_target_date = '2008-10-07'
def default_target_limit_time(target_direction):
    if target_direction == 'arrive_by':
        return 0 # 00:00
    elif target_direction == 'depart_after':
        return 1439 # 23:59
    else:
        assert False

# Display times after midnight for web display
def format_time(mins_after_midnight):
    hours = mins_after_midnight / 60
    mins = mins_after_midnight % 60
    if hours == 12 and mins == 0:
        return 'noon'
    suffix = hours < 12 and 'am' or 'pm'
    hours = hours % 12
    if hours == 0:
        hours = 12
    time = str(hours)
    if mins:
        time += ':%02d' % mins
    time += suffix
    return time

# Display vehicle type for web display
def pretty_vehicle_code(vehicle_code):
    if vehicle_code == 'T':
        return "Train";
    elif vehicle_code == 'B':
        return "Bus";
    elif vehicle_code == 'C':
        return "Coach";
    elif vehicle_code == 'M':
        return "Metro";
    elif vehicle_code == 'A':
        return "Air";
    elif vehicle_code == 'F':
        return "Ferry";
    else:
        assert False;

# Constants from cpplib/makeplan.h
JOURNEY_NULL = -1
JOURNEY_ALREADY_THERE = -2
JOURNEY_WALK = -3

LOCATION_NULL = -1
LOCATION_TARGET = 0

# Extracts time taken for a particular station from the .iso binary file of route times
def look_up_time_taken(map_id, station_id):
    iso_file = tmpwork + "/" + repr(map_id) + ".iso"
    isof = open(iso_file, 'rb')
    isof.seek(station_id * 2)
    tim = struct.unpack("h", isof.read(2))[0]
    return tim

# Extracts the next/previous route point from the .iso.routes binary file
def look_up_route_node(map_id, station_id):
    iso_file = tmpwork + "/" + repr(map_id) + ".iso.routes"
    isof = open(iso_file, 'rb')
    isof.seek(station_id * 8)
    location_id = struct.unpack("i", isof.read(4))[0]
    journey_id = struct.unpack("i", isof.read(4))[0]
    return (location_id, journey_id)


