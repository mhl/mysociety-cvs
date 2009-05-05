#
# makeplan.py:
# Make maps of journey times from NPTDR public transport route data.
#
# Copyright (c) 2008 UK Citizens Online Democracy. All rights reserved.
# Email: francis@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: makeplan.py,v 1.53 2009-05-05 18:15:59 francis Exp $
#

'''Finds shortest route from all points on a public transport network to arrive
at a given destination at a given time. Uses Dijkstra's algorithm to do this
all in one go.


A Railway Story
===============

Thomas was a cheeky tank engine who worked on the island of Sodor. He had a
branch line all to himself. 

The fat director made sure that passengers would always know when Thomas would
be at each station. He published the North Western Railway timetable for free
in the ATCO-CIF file format.

#>>> logging.basicConfig(level=logging.getLevelName('DEBUG'))

>>> atco = PlanningATCO() # PlanningATCO is derived from mysociety.atcocif.ATCO
>>> atco.read(sys.path[0] + "/fixtures/thomas-branch-line.cif")

Thomas proudly puffs up and down through six stations. 
>>> [ location.long_description() for location in atco.locations if location.point_type == 'R' ]
['Knapford Rail Station, Knapford, Sodor', 'Dryaw Rail Station, Dryaw, Sodor', 'Toryreck Rail Station, Toryreck, Sodor', 'Elsbridge Rail Station, Elsbridge, Sodor', 'Hackenbeck Rail Station, Hackenbeck, Sodor', 'Ffarquhar Rail Station, Ffarquhar, Sodor', 'Vicarstown Rail Station, Vicarstown, Sodor', 'Ballahoo Rail Station, Ballahoo, Sodor', 'Norramby Rail Station, Norramby, Sodor', "Crovan's Gate Rail Station, Crovan's Gate, Sodor"]

On weekdays he makes four journeys a day, two there, and two back.
>>> monday = datetime.date(2007,1,8)
>>> [ journey.route_direction for journey in atco.journeys 
...   if journey.is_valid_on_date(monday) and journey.operator == 'NWR' ]
['O', 'I', 'O', 'I', 'O', 'I', 'O']

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
[('TORYRECK', datetime.datetime(2007, 1, 8, 8, 0)), ('DRYAW', datetime.datetime(2007, 1, 8, 7, 20)), ('KNAPFORD', datetime.datetime(2007, 1, 8, 7, 0))]

routes gave her details of the best route she could take from each station. A
route consisted of a list of place/times, in reverse order starting with the
target destination, and ending with the place/time that appeared in the results
dictionary.
>>> print atco.pretty_print_routes(results, routes),
Journey times to TORYRECK by 08:00:00
From TORYRECK in 0 mins:
    You've arrived at TORYRECK
From DRYAW in 40 mins:
    Leave DRYAW by train on NWR-TT01 at 07:20:00, arriving TORYRECK at 07:45:00
    You've arrived at TORYRECK
From KNAPFORD in 60 mins:
    Leave KNAPFORD by train on NWR-TT01 at 07:00:00, arriving TORYRECK at 07:45:00
    You've arrived at TORYRECK

A second passenger wanted to be in Dryaw at 7:22 for breakfast with a friend.
The 7:00 from Knapford arrives at Dryaw at 7:20, so that train should be
returned as a result. Also a test that checks interchange times in the middle
of journeys, plus you can walk from Toryreck in 50 minutes!

>>> ch = logging.StreamHandler()
>>> (results, routes) = atco.do_dijkstra("DRYAW", datetime.datetime(2007,1,8, 7,22))
>>> results
[('DRYAW', datetime.datetime(2007, 1, 8, 7, 22)), ('KNAPFORD', datetime.datetime(2007, 1, 8, 7, 0)), ('TORYRECK', datetime.datetime(2007, 1, 8, 6, 32))]
>>> (results, routes) = atco.do_dijkstra("DRYAW", datetime.datetime(2007,1,8, 7,25))
>>> results
[('DRYAW', datetime.datetime(2007, 1, 8, 7, 25)), ('KNAPFORD', datetime.datetime(2007, 1, 8, 7, 0)), ('TORYRECK', datetime.datetime(2007, 1, 8, 6, 35))]

The Anopha Quarry manager wanted to get to work by 9:15am. He had to get a bus
from the end of the railway line.

>>> (results, routes) = atco.do_dijkstra('ANOPHAB', datetime.datetime(2007, 1, 8, 9, 15))
>>> results
[('ANOPHAB', datetime.datetime(2007, 1, 8, 9, 15)), ('FFARQUHARB', datetime.datetime(2007, 1, 8, 8, 50)), ('FFARQUHAR', datetime.datetime(2007, 1, 8, 8, 49)), ('HACKENBECK', datetime.datetime(2007, 1, 8, 8, 32)), ('ELSBRIDGE', datetime.datetime(2007, 1, 8, 8, 11)), ('TORYRECK', datetime.datetime(2007, 1, 8, 7, 45)), ('DRYAW', datetime.datetime(2007, 1, 8, 7, 20)), ('KNAPFORD', datetime.datetime(2007, 1, 8, 7, 0))]
>>> print atco.pretty_print_routes(results, routes),
Journey times to ANOPHAB by 09:15:00
From ANOPHAB in 0 mins:
    You've arrived at ANOPHAB
From FFARQUHARB in 25 mins:
    Leave FFARQUHARB by bus on NWRB-TT01 at 08:50:00, arriving ANOPHAB at 09:05:00
    You've arrived at ANOPHAB
From FFARQUHAR in 26 mins:
    Leave by walking to FFARQUHARB, will take 1 mins
    Leave FFARQUHARB by bus on NWRB-TT01 at 08:50:00, arriving ANOPHAB at 09:05:00
    You've arrived at ANOPHAB
From HACKENBECK in 43 mins:
    Leave HACKENBECK by train on NWR-TT01 at 08:32:00, arriving FFARQUHAR at 08:41:00
    Leave by walking to FFARQUHARB, will take 1 mins
    Leave FFARQUHARB by bus on NWRB-TT01 at 08:50:00, arriving ANOPHAB at 09:05:00
    You've arrived at ANOPHAB
From ELSBRIDGE in 64 mins:
    Leave ELSBRIDGE by train on NWR-TT01 at 08:11:00, arriving FFARQUHAR at 08:41:00
    Leave by walking to FFARQUHARB, will take 1 mins
    Leave FFARQUHARB by bus on NWRB-TT01 at 08:50:00, arriving ANOPHAB at 09:05:00
    You've arrived at ANOPHAB
From TORYRECK in 90 mins:
    Leave TORYRECK by train on NWR-TT01 at 07:45:00, arriving FFARQUHAR at 08:41:00
    Leave by walking to FFARQUHARB, will take 1 mins
    Leave FFARQUHARB by bus on NWRB-TT01 at 08:50:00, arriving ANOPHAB at 09:05:00
    You've arrived at ANOPHAB
From DRYAW in 115 mins:
    Leave DRYAW by train on NWR-TT01 at 07:20:00, arriving FFARQUHAR at 08:41:00
    Leave by walking to FFARQUHARB, will take 1 mins
    Leave FFARQUHARB by bus on NWRB-TT01 at 08:50:00, arriving ANOPHAB at 09:05:00
    You've arrived at ANOPHAB
From KNAPFORD in 135 mins:
    Leave KNAPFORD by train on NWR-TT01 at 07:00:00, arriving FFARQUHAR at 08:41:00
    Leave by walking to FFARQUHARB, will take 1 mins
    Leave FFARQUHARB by bus on NWRB-TT01 at 08:50:00, arriving ANOPHAB at 09:05:00
    You've arrived at ANOPHAB


Holiday makers from The Other Railway want to lie on the beach at Norramby.
James the Red Engine is currently on duty.

>>> (results, routes) = atco.do_dijkstra('NORRAMBY', datetime.datetime(2007, 1, 8, 12, 0))
>>> results
[('NORRAMBY', datetime.datetime(2007, 1, 8, 12, 0)), ('BALLAHOO', datetime.datetime(2007, 1, 8, 11, 30)), ('CROVANSGATE', datetime.datetime(2007, 1, 8, 11, 15)), ('VICARSTOWN', datetime.datetime(2007, 1, 8, 10, 50))]

>>> (results, routes) = atco.do_dijkstra('NORRAMBY', datetime.datetime(2007, 1, 8, 11, 0))
>>> results
[('NORRAMBY', datetime.datetime(2007, 1, 8, 11, 0)), ('BALLAHOO', datetime.datetime(2007, 1, 8, 10, 35)), ('VICARSTOWN', datetime.datetime(2007, 1, 8, 10, 0))]

>>> (results, routes) = atco.do_dijkstra('VICARSTOWN', datetime.datetime(2007, 1, 8, 13, 0))
>>> results
[('VICARSTOWN', datetime.datetime(2007, 1, 8, 13, 0)), ('BALLAHOO', datetime.datetime(2007, 1, 8, 12, 0)), ('NORRAMBY', datetime.datetime(2007, 1, 8, 11, 45)), ('CROVANSGATE', datetime.datetime(2007, 1, 8, 11, 40))]

>>> (results, routes) = atco.do_dijkstra('BALLAHOO', datetime.datetime(2007, 1, 8, 10, 40))
>>> results
[('BALLAHOO', datetime.datetime(2007, 1, 8, 10, 40)), ('VICARSTOWN', datetime.datetime(2007, 1, 8, 10, 0))]

>>> (results, routes) = atco.do_dijkstra('BALLAHOO', datetime.datetime(2007, 1, 8, 12, 10))
>>> results
[('BALLAHOO', datetime.datetime(2007, 1, 8, 12, 10)), ('NORRAMBY', datetime.datetime(2007, 1, 8, 11, 45)), ('CROVANSGATE', datetime.datetime(2007, 1, 8, 11, 15)), ('VICARSTOWN', datetime.datetime(2007, 1, 8, 10, 50))]


References regarding the North Western Railway:

Link to map of full network http://en.wikipedia.org/wiki/Sodor_(fictional_island)
http://en.wikipedia.org/wiki/North_Western_Railway_(fictional)#Thomas.27_Branch_Line
Station locations based on Wikipedia map using a ruler, Barrow being at 320k,470k, Douglas at 238k,476k.


Notes on using with NPTDR data
==============================

2008 data is valid in week 6-12 October 2008 only.

Routing does not allow for train routing guides or easements - the journeys
generated are possible, but you have to buy the right ticket(s).

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

    def __init__(self, general_interchange_default = 5, bus_interchange_default = 1):
        '''Create object that generates shortest journey times for all stations
        in a public transport network defined by an ATCO-CIF timetable file.

        general_interchange_default - time in minutes to allow by default to change trains etc. at one station
        bus_interchange_default - likewise for buses, at exact same stop
        '''

        self.general_interchange_default = general_interchange_default
        self.bus_interchange_default = bus_interchange_default
        mysociety.atcocif.ATCO.__init__(self)

    def print_journeys_crossing_midnight(self):
        '''Look for journeys that cross midnight, and print out a list.'''

        for journey in self.journeys:
            if journey.crosses_midnight():
                print "journey " + journey.id + " spans midnight"

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

    def _walk_time_apart(self, dist):
        '''How long it takes to walk between two stations dist distance apart.
        '''
        sec = float(dist) / float(self.walk_speed)
        # round up to nearest minute
        mins = int((sec + 59) / 60)
        walk_time = datetime.timedelta(seconds = mins * 60)
        return walk_time 

    def _nearby_locations(self, target_location, target_arrival_datetime, adjacents):
        '''Private function, called by adjacent_location_times. Looks for
        stations you can walk from to get to the target station.  This is
        constrained by self.walk_speed and self.walk_time. Adds any such
        stations to the adjacents structure.
        '''
        target_easting = self.location_from_id[target_location].additional.grid_reference_easting
        target_northing = self.location_from_id[target_location].additional.grid_reference_northing

        for location, dist in self.nearby_locations[self.location_from_id[target_location]].iteritems():
            logging.debug("_nearby_locations: %s (%d,%d) is %d away from %s (%d,%d)" % (location, location.additional.grid_reference_easting, location.additional.grid_reference_northing, dist, target_location, target_easting, target_northing))
            walk_time = self._walk_time_apart(dist)
            walk_departure_datetime = target_arrival_datetime - walk_time
            arrive_place_time = ArrivePlaceTime(location.location, walk_departure_datetime, onwards_leg_type = 'walk', onwards_walk_time = walk_time)
            # Use this location if new, or if it is later departure time than any previous one the same we've found.
            self._add_to_adjacents(arrive_place_time, adjacents)

    # How long after a journey it takes to interchange to catch another form of
    # transport at the given destination stop.
    def _interchange_time_after_journey(self, journey, location):
        # Work out type of next onwards journey
        onwards_arrive_place_time = self._settled_routes[location][0]
        onwards_leg_type = onwards_arrive_place_time.onwards_leg_type 

        if onwards_leg_type == 'already_there':
            # No interchange time at the end
            assert location == self.final_destination
            return 0
        elif onwards_leg_type == 'walk':
            # No interchange time if walking
            return 0

        # Look up before and after vehicle code types
        assert onwards_leg_type == 'journey'
        onwards_journey = onwards_arrive_place_time.onwards_journey
        vehicle_code = journey.vehicle_code(self)
        onwards_vehicle_code = onwards_journey.vehicle_code(self)

        # Base interchange time on vehicle type
        if vehicle_code == 'B' and onwards_vehicle_code == 'B':
            return self.bus_interchange_default
        else:
            return self.general_interchange_default

    # Name of vehicle type for journey
    def _vehicle_type_name_for_journey(self, journey):
        vehicle_code = journey.vehicle_code(self)

        if vehicle_code == 'T':
            return "train"
        elif vehicle_code == 'B':
            return "bus"
        elif vehicle_code == 'C':
            return "coach"
        elif vehicle_code == 'M':
            return "metro"
        elif vehicle_code == 'A':
            return "air"
        elif vehicle_code == 'F':
            return "ferry"
        else:
            raise Exception("Unknown vehicle code " + str(vehicle_code))

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
            return

        # Find out when it arrives at this stop (can be multiple times for looped journeys)
        arrival_times_at_target_location = journey.find_arrival_times_at_location(target_location)
        if not arrival_times_at_target_location:
            # could never arrive at this stop (even though was in journeys_visiting_location),
            # e.g. for pick up only stops
            return

        logging.debug("\t\tarrival times at target location: " + str(arrival_times_at_target_location))

        # Work out how long we need to allow to change at the stop
        interchange_time_in_minutes = self._interchange_time_after_journey(journey, target_location)
        interchange_time = datetime.timedelta(minutes = interchange_time_in_minutes)
        
        # Pick the latest of the arrival times that's before the time we're
        # currently at (plus interchange time of course). Usually there'll only
        # be one of these, but there can be more for looped journeys.
        arrival_datetime_at_target_location = None
        for arrival_time_at_target_location in arrival_times_at_target_location:
            possible_arrival_datetime_at_target_location = datetime.datetime.combine(target_arrival_datetime.date(), arrival_time_at_target_location)
            if possible_arrival_datetime_at_target_location + interchange_time <= target_arrival_datetime and (arrival_datetime_at_target_location is None or arrival_datetime_at_target_location < possible_arrival_datetime_at_target_location):
                arrival_datetime_at_target_location = possible_arrival_datetime_at_target_location

        # See whether if we want to use this journey to get to this
        # stop, we get there on time to change to the next journey.
        if not arrival_datetime_at_target_location:
            logging.debug("\t\twhich are all too late with interchange time %s, so not using journey" % str(interchange_time))
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
            # Ignore the target location
            if hop.location == target_location:
                continue

            # If the stop doesn't pick up passengers, don't use it
            if not hop.is_pick_up():
                continue

            departure_datetime = datetime.datetime.combine(target_arrival_datetime.date(), hop.published_departure_time)

            # If the time at this hop is later than at target, we stop.
            # We use time for this, rather than stopping at the target location,
            # so we cope with looped journeys.
            # XXX This will also stop midnight rollover journeys at midnight.
            # If we care about maps near midnight, then this needs fixing by
            # duplicating the journey at an earlier stage in processing, as
            # well as by working out the right date/time in
            # _adjacent_location_times_for_journey to get is_valid_on_date
            # right.
            if departure_datetime > arrival_datetime_at_target_location:
                break

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

        Returns (results, routes) where:

        results - is an array of pairs of station identifier, date/time at that
            station, in order starting with the station that is quickest to get
            to the destination.
        routes - a dictionary from a station identifier, to the more detailed
            route to take to get to it.
        '''

        # Check precompute_for_dijkstra was called with same parameters for
        # those that matter
        assert self.nearby_max_distance == walk_speed * walk_time

        # The thing we're going to use for priority in the pqueue
        class Priority:
            def __init__(self, when, name):
                self.when = when
                self.name = name
            # operator just for use on priority queue
            def __cmp__(self, other):
                # The priority queue pops smallest first, whereas we want
                # largest, so these are reversed from expected direction
                if self.when < other.when:
                    return 1
                elif self.when > other.when:
                    return -1
                elif self.when == other.when:
                    # if the two are the same priority time, we sort by 
                    # alphabetical order of station name for stability
                    if self.name > other.name:
                        return 1
                    elif self.name < other.name:
                        return -1
                    elif self.name == other.name:
                        return 0 
                    assert False
                assert False
            def __repr__(self):
                return "Priority(" + repr(self.when) + ", " + repr(self.name) + ")"

       
        # Set up initial state
        settled_in_order = []
        settled_set = set() # dictionary from location to datetime
        self._settled_routes = {} # routes of settled journeys
        queue = pqueue.PQueue()
        queue.insert(Priority(target_datetime, target_location), target_location)
        routes = {}
        routes[target_location] = [ ArrivePlaceTime(target_location, target_datetime, onwards_leg_type = 'already_there') ] # how to get there
        self.final_destination = target_location
        self.final_datetime = target_datetime
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
            settled_set.add(nearest_location)
            settled_in_order.append((nearest_location, nearest_datetime))
            # ... copy the route into settled_routes, so we only return routes
            # we know we finished (rather than the partial, best-so-far that is
            # in routes)
            self._settled_routes[nearest_location] = routes[nearest_location]
            logging.info("settled " + nearest_location + " " + str(nearest_datetime))
            
            # Add all of its neighbours to the queue
            foundtimes = self.adjacent_location_times(nearest_location, nearest_datetime)
            for location, arrive_place_time in foundtimes.iteritems():
                new_priority = Priority(arrive_place_time.when, arrive_place_time.location)
                try:
                    # See if this location is already in queue 
                    current_priority = queue[location]
                    # If we get here then it is, see if what we found is nearer and update priority
                    assert location not in settled_set
                    if new_priority < current_priority:
                        queue[location] = new_priority
                        routes[location] = [ arrive_place_time ] + routes[nearest_location] 
                        logging.debug("updated " + location + " from priority " + str(current_priority) + " to " + str(new_priority) + " in queue")
                except KeyError, e: # only way of testing presence in queue is to catch an exception
                    if location not in settled_set:
                        # No existing entry for location in queue
                        queue.insert(new_priority, location)
                        routes[location] = [ arrive_place_time ] + routes[nearest_location] 
                        logging.debug("added " + location + " " + str(new_priority) + " to queue")

        return (settled_in_order, self._settled_routes)

    def pretty_print_routes(self, results, routes):
        '''do_dijkstra returns a journey routes array, this prints it in a human readable format.'''

        ret = "Journey times to " + self.final_destination + " by " + str(self.final_datetime.time()) + "\n"

        for place, when in results:
            route = routes[place]
            mins = int((self.final_datetime - when).seconds / 60.0);
            ret += "From " + place + " in " + str(mins) + " mins:\n"
            for ix in range(len(route)):
                stop = route[ix]
                if stop.onwards_leg_type == 'already_there':
                    ret += "    You've arrived at " + stop.location + "\n"
                    continue
                next_stop = route[ix + 1]
                
                if stop.onwards_leg_type == 'walk':
                    ret += "    Leave by walking to %s, will take %d mins\n" % (next_stop.location, int(stop.onwards_walk_time.seconds / 60.0))
                elif stop.onwards_leg_type == 'journey':
                    departure_times = stop.onwards_journey.find_departure_times_at_location(stop.location)
                    departure_time = []
                    for a in departure_times:
                        departure_time.append(a.strftime("%H:%M:%S"))
                    arrival_times = stop.onwards_journey.find_arrival_times_at_location(next_stop.location)
                    arrival_time = []
                    for a in arrival_times:
                        arrival_time.append(a.strftime("%H:%M:%S"))
                    ret += "    Leave " + stop.location + " by " + self._vehicle_type_name_for_journey(stop.onwards_journey) + " on " + stop.onwards_journey.id + " at " + ','.join(departure_time) + ", arriving " + next_stop.location + " at " + ','.join(arrival_time) + "\n"
                else:
                    raise Exception, "Unknown leg type '" + stop.onwards_leg_type + "'"

        return ret

if __name__ == "__main__":
    import doctest
    doctest.testmod()

