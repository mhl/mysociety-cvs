#
# makeplan.py:
# Make maps of journey times from NPTDR public transport route data.
#
# Copyright (c) 2008 UK Citizens Online Democracy. All rights reserved.
# Email: francis@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: makeplan.py,v 1.35 2009-03-03 16:11:28 francis Exp $
#

# TODO:
# Rename this planningatco.py
#
# Instead of inheriting from atcocif, have it as a member? so can keep caches more than one run
# Think about idempotency if atcocif.ignored variable
#
# timetz - what about time zones!  http://docs.python.org/lib/datetime-datetime.html
#
# Make sure there is a test for proximity interchanging
#
# Journeys over midnight are knackered
#  - journeys crossing midnight count for the earlier day 
#  - we have to load them twice, once for each? is there more general problem that
#    we have to load all journeys on today and yesterday? all once with a later
#    hour anyway :)
#  - in particular, which day are journeys starting just after midnight stored for?
#  - see "XXX bah" below for hack that will do for now but NEEDS CHANGING
#
# Check circular journeys work fine
#
# Check the date of week data is valid for, to be sure
#
# Interchange times
# - find proper ones to use for TRAIN and BUS
# - possibly load QV records if needed to discriminate times
# - need another longer time for QVNAIR/12?
# - measures according to type of journey before, not pair of before/after
#
# Get rid of index_by_short_codes somehow
#
# Optimisation
# ============
# Remove squareroot in distance calculation
# Have a sorted grid to find nearby stations more quickly
# Perhaps just precalculate nearby stations for each station
#
# Use objects for locations wherever possible, so less dictionary lookups by string
#
# Can use bisect to calculate find_arrival_time_at_location (or that will be
# subsumed by some other cache)
#
# For each station, have every station that you can get there from directly,
# and all their times, indexed by time so can instantly get list of best times
# to leave to arrive by particular time
#
# Find out how to profile memory use in Python
# Work out minimum structure could export to run C++ algorithm on
# 

'''Finds shortest route from all points on a public transport network to arrive
at a given destination at a given time. Uses Dijkstra's algorithm to do this
all in one go.

Notes: Does not allow for train routing guides or easements - the journeys
generated are possible, but you have to buy the right ticket(s).


A Railway Story
===============

Thomas was a cheeky tank engine who worked on the island of Sodor. He had a
branch line all to himself. 

The fat director made sure that passengers would always know when Thomas would
be at each station. He published the North Western Railway timetable for free
in the ATCO-CIF file format.

>>> atco = PlanningATCO() # PlanningATCO is derived from mysociety.atcocif.ATCO
>>> atco.read(sys.path[0] + "/fixtures/thomas-branch-line.cif")

Thomas proudly puffs up and down through six stations. 
>>> [ location.long_description() for location in atco.locations if location.point_type == 'R' ]
['Knapford Rail Station, Knapford, Sodor', 'Dryaw Rail Station, Dryaw, Sodor', 'Toryreck Rail Station, Toryreck, Sodor', 'Elsbridge Rail Station, Elsbridge, Sodor', 'Hackenbeck Rail Station, Hackenbeck, Sodor', 'Ffarquhar Rail Station, Ffarquhar, Sodor']

On weekdays he makes four journeys a day, two there, and two back.
>>> monday = datetime.date(2007,1,8)
>>> [ journey.route_direction for journey in atco.journeys 
...   if journey.is_valid_on_date(monday) and journey.operator == 'NWR' ]
['O', 'I', 'O', 'I']

On Sundays he makes only one trip there and back.
>>> sunday = datetime.date(2007,1,14)
>>> [ journey.route_direction for journey in atco.journeys 
...   if journey.is_valid_on_date(sunday) ]
['O', 'I']

There was a passenger who had a new job at the Lead and Uranium mines near
Toryreck. She wanted to know where she could live, and arrive in time for work
at 8am by train.

First she made indices of all the journeys and stations, and worked out which
she could walk between.
>>> atco.precompute_for_dijkstra()

Then she called do_dijkstra to find out all the best routes that arrive from
every place in the network at Toryreck by 8am on a Monday. She was given a
results and a routes data structure in return.
>>> (results, routes) = atco.do_dijkstra("TORYRECK", datetime.datetime(2007,1,8, 8,0))

results contained a dictionary with each station on the network from which she
can arrive at work on time, and the latest time at which you need to leave that
station.
>>> results
{'DRYAW': datetime.datetime(2007, 1, 8, 7, 20), 'TORYRECK': datetime.datetime(2007, 1, 8, 8, 0), 'KNAPFORD': datetime.datetime(2007, 1, 8, 7, 0)}

routes gave her details of the best route she could take from each station. A
route consisted of a list of place/times, in reverse order starting with the
target destination, and ending with the place/time that appeared in the results
dictionary.
>>> atco.pretty_print_routes(routes)
From DRYAW:
    Leave DRYAW by TRAIN on the 07:20:00, arriving TORYRECK at 07:45:00
    You've arrived at TORYRECK
From TORYRECK:
    You've arrived at TORYRECK
From KNAPFORD:
    Leave KNAPFORD by TRAIN on the 07:00:00, arriving TORYRECK at 07:45:00
    You've arrived at TORYRECK

A second passenger wanted to be in Dryaw at 7:22 for breakfast with a friend.
The 7:00 from Knapford arrives at Dryaw at 7:20, so that train should be
returned as a result. Also a test that checks interchange times in the middle
of journeys, plus you can walk from Toryreck in 50 minutes!

>>> ch = logging.StreamHandler()
>>> (results, routes) = atco.do_dijkstra("DRYAW", datetime.datetime(2007,1,8, 7,22))
>>> results
{'DRYAW': datetime.datetime(2007, 1, 8, 7, 22), 'TORYRECK': datetime.datetime(2007, 1, 8, 6, 32), 'KNAPFORD': datetime.datetime(2007, 1, 8, 7, 0)}
>>> (results, routes) = atco.do_dijkstra("DRYAW", datetime.datetime(2007,1,8, 7,25))
>>> results
{'DRYAW': datetime.datetime(2007, 1, 8, 7, 25), 'TORYRECK': datetime.datetime(2007, 1, 8, 6, 35), 'KNAPFORD': datetime.datetime(2007, 1, 8, 7, 0)}


The Anopha Quarry manager wanted to get to work by 9:15am. He had to get a bus
from the end of the railway line.

>>> (results, routes) = atco.do_dijkstra('ANOPHAB', datetime.datetime(2007, 1, 8, 9, 15))
>>> results
{'FFARQUHARB': datetime.datetime(2007, 1, 8, 8, 50), 'HACKENBECK': datetime.datetime(2007, 1, 8, 8, 32), 'TORYRECK': datetime.datetime(2007, 1, 8, 7, 45), 'DRYAW': datetime.datetime(2007, 1, 8, 7, 20), 'FFARQUHAR': datetime.datetime(2007, 1, 8, 8, 49, 6, 148352), 'ELSBRIDGE': datetime.datetime(2007, 1, 8, 8, 11), 'ANOPHAB': datetime.datetime(2007, 1, 8, 9, 15), 'KNAPFORD': datetime.datetime(2007, 1, 8, 7, 0)}
>>> atco.pretty_print_routes(routes)
From FFARQUHARB:
    Leave FFARQUHARB by BUS on the 08:50:00, arriving ANOPHAB at 09:05:00
    You've arrived at ANOPHAB
From HACKENBECK:
    Leave HACKENBECK by TRAIN on the 08:32:00, arriving FFARQUHAR at 08:41:00
    Leave by walking to FFARQUHARB, will take 0 mins
    Leave FFARQUHARB by BUS on the 08:50:00, arriving ANOPHAB at 09:05:00
    You've arrived at ANOPHAB
From TORYRECK:
    Leave TORYRECK by TRAIN on the 07:45:00, arriving FFARQUHAR at 08:41:00
    Leave by walking to FFARQUHARB, will take 0 mins
    Leave FFARQUHARB by BUS on the 08:50:00, arriving ANOPHAB at 09:05:00
    You've arrived at ANOPHAB
From DRYAW:
    Leave DRYAW by TRAIN on the 07:20:00, arriving FFARQUHAR at 08:41:00
    Leave by walking to FFARQUHARB, will take 0 mins
    Leave FFARQUHARB by BUS on the 08:50:00, arriving ANOPHAB at 09:05:00
    You've arrived at ANOPHAB
From FFARQUHAR:
    Leave by walking to FFARQUHARB, will take 0 mins
    Leave FFARQUHARB by BUS on the 08:50:00, arriving ANOPHAB at 09:05:00
    You've arrived at ANOPHAB
From ELSBRIDGE:
    Leave ELSBRIDGE by TRAIN on the 08:11:00, arriving FFARQUHAR at 08:41:00
    Leave by walking to FFARQUHARB, will take 0 mins
    Leave FFARQUHARB by BUS on the 08:50:00, arriving ANOPHAB at 09:05:00
    You've arrived at ANOPHAB
From ANOPHAB:
    You've arrived at ANOPHAB
From KNAPFORD:
    Leave KNAPFORD by TRAIN on the 07:00:00, arriving FFARQUHAR at 08:41:00
    Leave by walking to FFARQUHARB, will take 0 mins
    Leave FFARQUHARB by BUS on the 08:50:00, arriving ANOPHAB at 09:05:00
    You've arrived at ANOPHAB


Todo cif file:
Check that all the ids and train operation numbers and stuff in journey parts are ok - I think that they are MPS
Add direct services to Tidmouth
Add some services run by Daisy on Thomas's line
Reduced Sunday service

Notes:
Link to map of full network http://en.wikipedia.org/wiki/Sodor_(fictional_island)
http://en.wikipedia.org/wiki/North_Western_Railway_(fictional)#Thomas.27_Branch_Line
Station locations based on Wikipedia map using a ruler, Barrow being at 320k,470k, Douglas at 238k,476k.
'''

import logging
import pqueue
import datetime
import sys
import os
import math

sys.path.append(sys.path[0] + "/../../pylib") # XXX this is for running doctests and is nasty, there's got to be a better way
import mysociety.atcocif

class ArrivePlaceTime:
    '''Stores a location and date/time of arrival (including interchange wait)
    at that location.'''

    def __init__(self, location, when, onwards_leg_type=None, onwards_journey=None, onwards_walk_time = None):
        self.location = location
        self.when = when
        self.onwards_leg_type = onwards_leg_type
        self.onwards_journey = onwards_journey
        self.onwards_walk_time = onwards_walk_time

    def __repr__(self):
        s = "ArrivePlaceTime(" + repr(self.location) + ", " + repr(self.when)
        if self.onwards_leg_type != None:
            s = s + ", " + repr(self.onwards_leg_type)
        if self.onwards_journey != None:
            s = s + ", onwards_journey=JourneyHeader(" + repr(self.onwards_journey.id) + ")"
        if self.onwards_walk_time != None:
            s = s + ", onwards_walk_time=" + repr(self.onwards_walk_time)
        s = s + ")"
        return s
      
class PlanningATCO(mysociety.atcocif.ATCO):
    '''Loads and represents a set of ATCO-CIF files, and can generate large
    sets of quickest routes from them.'''

    def __init__(self, train_interchange_default = 5, bus_interchange_default = 1):
        '''Create object that generates shortest journey times for all stations
        in a public transport network defined by an ATCO-CIF timetable file.

        train_interchange_default - time in minutes to allow by default to change trains at same station
        bus_interchange_default - likewise for buses, at exact same stop
        '''

        self.train_interchange_default = train_interchange_default
        self.bus_interchange_default = bus_interchange_default
        mysociety.atcocif.ATCO.__init__(self)

    def find_journeys_crossing_midnight(self):
        '''Look for journeys that cross midnight, and print out a list.'''

        for journey in self.journeys:
            previous_departure_time = datetime.time(0, 0, 0)
            for hop in journey.hops:
                if hop.is_pick_up():
                    if previous_departure_time > hop.published_departure_time:
                        print "journey " + journey.id + " spans midnight"
                    previous_departure_time = hop.published_departure_time

    def adjacent_location_times(self, target_location, target_arrival_datetime):
        '''Adjacency function for use with Dijkstra's algorithm on earliest
        time to arrive somewhere.  Given a location (string short code) and a
        date/time, it finds every other station from which you can get there on
        time by one *direct* train/bus. The return value is a dictionary from
        the station short code to the date/time - so each station only appears
        once. 
        '''

        # Check that there are journeys visiting this location
        logging.debug("adjacent_location_times target_location: " + target_location + " target_arrival_datetime: " + str(target_arrival_datetime))
        if target_location not in self.journeys_visiting_location:
            raise Exception, "No journeys known visiting target_location " + target_location

        # Adjacents is dictionary from location to time at that location, and
        # is the data structure we are going to return from this function.
        adjacents = {}
        # Go through every journey visiting the location
        for journey in self.journeys_visiting_location[target_location]:
            if journey.ignored: continue
            logging.debug("\tconsidering journey: " + journey.id)
            self._adjacent_location_times_for_journey(target_location, target_arrival_datetime, adjacents, journey)
        self._nearby_locations(target_location, target_arrival_datetime, adjacents)
        return adjacents

    def _add_to_adjacents(self, arrive_place_time, adjacents):
        '''Private helper function. Store a time we can leave a station, if it
        is later than previous direct routes we have for leaving from that
        station and arriving at target.'''
        if arrive_place_time.location in adjacents:
            curr_latest = adjacents[arrive_place_time.location]
            if arrive_place_time.when > curr_latest.when:
                adjacents[arrive_place_time.location] = arrive_place_time
        else:
            adjacents[arrive_place_time.location] = arrive_place_time

    def _nearby_locations(self, target_location, target_arrival_datetime, adjacents):
        '''Private function, called by adjacent_location_times. Looks for
        stations you can walk from to get to the target station.  This is
        constrained by self.walk_speed and self.walk_time. Adds any such
        stations to the adjacents structure.
        '''

        try:
            target_easting = self.location_details[target_location].additional.grid_reference_easting
            target_northing = self.location_details[target_location].additional.grid_reference_northing
        except AttributeError, e:
            return

        for location, dist in self.nearby_locations[self.location_details[target_location]].iteritems():
            logging.debug("%s (%d,%d) is %d away from %s (%d,%d)" % (location, location.additional.grid_reference_easting, location.additional.grid_reference_northing, dist, target_location, target_easting, target_northing))
            walk_time = datetime.timedelta(seconds = dist / self.walk_speed)
            walk_departure_datetime = target_arrival_datetime - walk_time
            arrive_time_place = ArrivePlaceTime(location.location, walk_departure_datetime, onwards_leg_type = 'walk', onwards_walk_time = walk_time)
            # Use this location if new, or if it is later departure time than any previous one the same we've found.
            self._add_to_adjacents(arrive_time_place, adjacents)

    def _adjacent_location_times_for_journey(self, target_location, target_arrival_datetime, adjacents, journey):
        '''Private function, called by adjacent_location_times. Finds every
        other station you can get to the destination on time, using
        the specific given bus/train in journey. Results are stored in the
        adjacents structure.
        '''

        # Check whether the journey runs on the relevant date
        # XXX assumes we don't do journeys over midnight
        valid_on_date = journey.is_valid_on_date(target_arrival_datetime.date()) 
        if not valid_on_date:
            logging.debug("\t\tnot valid on date: " + valid_on_date.reason)
            journey.ignore()
            return

        # Find out when it arrives at this stop
        arrival_time_at_target_location = journey.find_arrival_time_at_location(target_location)
        if arrival_time_at_target_location == None:
            # could never arrive at this stop (even though was in journeys_visiting_location),
            # e.g. for pick up only stops
            return

        logging.debug("\t\tarrival time at target location: " + str(arrival_time_at_target_location))
        arrival_datetime_at_target_location = datetime.datetime.combine(target_arrival_datetime.date(), arrival_time_at_target_location)

        # Work out how long we need to allow to change at the stop
        if target_location == self.final_destination:
            interchange_time_in_minutes = 0
        elif journey.vehicle_type == 'TRAIN':
            interchange_time_in_minutes = self.train_interchange_default
        else: # Bus, Air, Metro/Tram, Ferry/River Bus XXX
            interchange_time_in_minutes = self.bus_interchange_default
        interchange_time = datetime.timedelta(minutes = interchange_time_in_minutes)
        
        # See whether if we want to use this journey to get to this
        # stop, we get there on time to change to the next journey.
        if arrival_datetime_at_target_location + interchange_time > target_arrival_datetime:
            logging.debug("\t\twhich is too late with interchange time %s, so not using journey" % str(interchange_time))
            return

        logging.debug("\t\tadding stops")
        self._adjacent_location_times_add_stops(target_location, target_arrival_datetime, adjacents, journey, arrival_datetime_at_target_location)

    def _adjacent_location_times_add_stops(self, target_location, target_arrival_datetime, adjacents, journey, arrival_datetime_at_target_location):
        '''Private function, called by _adjacent_location_times_for_journey.
        For a given journey, adds individual stops which are valid to the
        adjacents structure.
        '''

        # Now go through every earlier stop, and add it to the list of returnable nodes
        for hop in journey.hops:
            # We've arrived at the target location (also check is_set_down
            # here, so looped/circular journeys, where we end on stop we
            # started, work)
            if hop.is_set_down() and hop.location == target_location:
                break

            # If the stop doesn't pick up passengers, don't use it
            if not hop.is_pick_up():
                continue

            departure_datetime = datetime.datetime.combine(target_arrival_datetime.date(), hop.published_departure_time)

            # if the time at this hop is later than at target, must be a midnight rollover, and really
            # this hop is on the the day before, so change to that
            # XXX bah this is rubbish as it won't have done the is right day check right in _adjacent_location_times_for_journey that called this
            if departure_datetime > arrival_datetime_at_target_location:
                departure_datetime = datetime.datetime.combine(target_arrival_datetime.date() - datetime.timedelta(1), hop.published_departure_time)
            # Use this location if new, or if it is later departure time than any previous one the same we've found.
            arrive_place_time = ArrivePlaceTime(hop.location, departure_datetime, onwards_leg_type = 'journey', onwards_journey = journey)
            self._add_to_adjacents(arrive_place_time, adjacents)

    def precompute_for_dijkstra(self, walk_speed=1, walk_time=3600):
        '''
        Call this before running Dijkstra's algorithm, to intialise everything. It only needs
        to be called once, if you're running the algorithm multiple times with the same
        parameters that this function takes.
        '''

        self.index_by_short_codes()
        self.index_nearby_locations(walk_speed * walk_time)
 
    def do_dijkstra(self, target_location, target_datetime, walk_speed=1, walk_time=3600, earliest_departure=None):
        '''
        Run Dijkstra's algorithm to find latest departure time from all locations to
        arrive at the target location by the given time.

        target_location - station id to go to, e.g. 9100AYLSBRY or 210021422650
        target_datetime - when we want to arrive by
        '''

        # Check precompute_for_dijkstra was called with same parameters for
        # those that matter
        assert self.nearby_max_distance == walk_speed * walk_time

        # The thing we're going to use for priority in the pqueue
        class Priority:
            def __init__(self, when):
                self.when = when
            # operator just for use on priority queue
            def __cmp__(self, other):
                # The priority queue pops smallest first, whereas we want
                # largest, so these are reversed from expected direction
                if self.when < other.when:
                    return 1
                if self.when == other.when:
                    return 0 
                if self.when > other.when:
                    return -1
                assert False
            def __repr__(self):
                return "Priority(" + repr(self.when) + ")"

       
        # Set up initial state
        settled = {} # dictionary from location to datetime
        settled_routes = {} # routes of settled journeys
        queue = pqueue.PQueue()
        queue.insert(Priority(target_datetime), target_location)
        routes = {}
        routes[target_location] = [ ArrivePlaceTime(target_location, target_datetime, onwards_leg_type = 'already_there') ] # how to get there
        self.final_destination = target_location
        self.walk_speed = walk_speed
        self.walk_time = walk_time

        while len(queue) > 0:
            # Find the item at top of queue
            (nearest_datetime, nearest_location) = queue.pop()
            nearest_datetime = nearest_datetime.when

            # If it is earlier than earliest departure we are going back to, then finish
            if earliest_departure and nearest_datetime < earliest_departure:
                break

            # That item is now settled
            settled[nearest_location] = nearest_datetime
            # ... copy the route into settled_routes, so we only return routes
            # we know we finished (rather than the partial, best-so-far that is
            # in routes)
            settled_routes[nearest_location] = routes[nearest_location]
            logging.info("settled " + nearest_location + " " + str(nearest_datetime))
            
            # Add all of its neighbours to the queue
            foundtimes = self.adjacent_location_times(nearest_location, nearest_datetime)
            for location, arrive_place_time in foundtimes.iteritems():
                new_priority = Priority(arrive_place_time.when)
                try:
                    # See if this location is already in queue 
                    current_priority = queue[location]
                    # If we get here then it is, see if what we found is nearer and update priority
                    assert location not in settled
                    if new_priority < current_priority:
                        queue[location] = new_priority
                        routes[location] = [ arrive_place_time ] + routes[nearest_location] 
                        logging.debug("updated " + location + " from priority " + str(current_priority) + " to " + str(new_priority) + " in queue")
                except KeyError, e: # only way of testing presence in queue is to catch an exception
                    if location not in settled:
                        # No existing entry for location in queue
                        queue.insert(new_priority, location)
                        routes[location] = [ arrive_place_time ] + routes[nearest_location] 
                        logging.debug("added " + location + " " + str(new_priority) + " to queue")

        return (settled, settled_routes)

    def pretty_print_routes(self, routes):
        '''do_dijkstra returns a journey routes array, this prints it in a human readable format.'''
        for place, route in routes.iteritems():
            print "From " + place + ":"
            for ix in range(len(route)):
                stop = route[ix]
                if stop.onwards_leg_type == 'already_there':
                    print "    You've arrived at " + stop.location
                    continue
                next_stop = route[ix + 1]
                
                if stop.onwards_leg_type == 'walk':
                    print "    Leave by walking to " + next_stop.location + ", will take " + str(stop.onwards_walk_time.seconds / 60) + " mins"
                elif stop.onwards_leg_type == 'journey':
                    departure_time = stop.onwards_journey.find_departure_time_at_location(stop.location)
                    arrival_time = stop.onwards_journey.find_arrival_time_at_location(next_stop.location)
                    print "    Leave " + stop.location + " by " + stop.onwards_journey.vehicle_type + " on the " + departure_time.strftime("%H:%M:%S") + ", arriving " + next_stop.location + " at " + arrival_time.strftime("%H:%M:%S")
                else:
                    raise "Unknown leg type '" + stop.onwards_leg_type + "'"

if __name__ == "__main__":
    import doctest
    doctest.testmod()

