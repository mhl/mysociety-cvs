#
# makeplan.py:
# Make maps of journey times from NPTDR public transport route data.
#
# Copyright (c) 2008 UK Citizens Online Democracy. All rights reserved.
# Email: francis@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: makeplan.py,v 1.15 2009-02-20 20:05:20 matthew Exp $
#

# TODO:
# Rename this planningatco.py
#
# timetz - what about time zones!  http://docs.python.org/lib/datetime-datetime.html
#
# The time of the last place in routes is a bit pants as it includes the wait!
#   MPS: Guess it needs to store arrival times too, and then use that for final leg
#
# Journeys over midnight will be knackered, no idea how ATCO-CIF even stores them
#  - in particular, which day are journeys starting just after midnight stored for?
#  - see "XXX bah" below for hack that will do for now but NEEDS CHANGING
#
# Check circular journeys work fine
#
# Interchange times
# - find proper ones to use for TRAIN and BUS
# - need another longer time for QVNAIR/12?
# - measures according to type of journey before, not pair of before/after
#
# Get rid of index_by_short_codes somehow
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
>>> [ location.long_description() for location in atco.locations ]
['Knapford Rail Station', 'Dryaw Rail Station', 'Toryreck Rail Station', 'Elsbridge Rail Station', 'Hackenbeck Rail Station', 'Ffarquhar Rail Station']

On weekdays he makes four journeys a day, two there, and two back.
>>> monday = datetime.date(2007,1,8)
>>> [ journey.route_direction for journey in atco.journeys 
...   if journey.is_valid_on_date(monday) ]
['O', 'I', 'O', 'I']

On Sundays he makes only one trip there and back.
>>> sunday = datetime.date(2007,1,14)
>>> [ journey.route_direction for journey in atco.journeys 
...   if journey.is_valid_on_date(sunday) ]
['O', 'I']

There was a passenger who had a new job at the Lead and Uranium mines near
Toryreck. She wanted to know where she could live, and arrive in time for work
at 8am by train.

First she made indices of all the journeys and stations.
>>> atco.index_by_short_codes()

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
>>> routes
{'DRYAW': [ArrivePlaceTime('TORYRECK', datetime.datetime(2007, 1, 8, 8, 0), interchange_wait=True), ArrivePlaceTime('DRYAW', datetime.datetime(2007, 1, 8, 7, 20), interchange_wait=True)], 'TORYRECK': [ArrivePlaceTime('TORYRECK', datetime.datetime(2007, 1, 8, 8, 0), interchange_wait=True)], 'KNAPFORD': [ArrivePlaceTime('TORYRECK', datetime.datetime(2007, 1, 8, 8, 0), interchange_wait=True), ArrivePlaceTime('KNAPFORD', datetime.datetime(2007, 1, 8, 7, 0), interchange_wait=True)]}

The 7:00 from Knapford arrives at Dryaw at 7:20, so test that asking for arrival
time of 7:22 (within the interchange time) works. Also a test that checks
interchange times in the middle of journeys.

>>> ch = logging.StreamHandler()
>>> (results, routes) = atco.do_dijkstra("DRYAW", datetime.datetime(2007,1,8, 7,22))
>>> results
{'DRYAW': datetime.datetime(2007, 1, 8, 7, 22), 'KNAPFORD': datetime.datetime(2007, 1, 8, 7, 0)}
>>> (results, routes) = atco.do_dijkstra("DRYAW", datetime.datetime(2007,1,8, 7,25))
>>> results
{'DRYAW': datetime.datetime(2007, 1, 8, 7, 25), 'KNAPFORD': datetime.datetime(2007, 1, 8, 7, 0)}


Todo cif file:
Check that all the ids and train operation numbers and stuff in journey parts are ok
Add direct services to Tidmouth
Add some services run by Daisy on Thomas's line
Reduced Sunday service
Link to map of full network http://en.wikipedia.org/wiki/Sodor_(fictional_island)
http://en.wikipedia.org/wiki/North_Western_Railway_(fictional)#Thomas.27_Branch_Line
'''

import logging
import pqueue
import datetime
import sys
import os
import math

sys.path.append(sys.path[0] + "/../../pylib") # XXX this is for running doctests and is nasty, there's got to be a better way
import mysociety.atcocif

# Stores a location and date/time of arrival at that location.
# If interchange_wait is True, then the time must be after a wait
# for changing to the next transport. If it is False, then there is no
# interchange wait (e.g. at the end of a journey).
class ArrivePlaceTime:
    def __init__(self, location, when, interchange_wait = True):
        self.location = location
        self.when = when
        self.interchange_wait = interchange_wait

    def __repr__(self):
        return "ArrivePlaceTime(" + repr(self.location) + ", " + repr(self.when) + ", interchange_wait=" + repr(self.interchange_wait) + ")"
      
# Loads and represents a set of ATCO-CIF files, and can generate large sets of
# quickest routes from them
class PlanningATCO(mysociety.atcocif.ATCO):
    # train_interchange_default - time in minutes to allow by default to change trains at same station
    # bus_interchange_default - likewise for buses, at exact same stop
    def __init__(self, train_interchange_default = 5, bus_interchange_default = 1):
        self.train_interchange_default = train_interchange_default
        self.bus_interchange_default = bus_interchange_default
        mysociety.atcocif.ATCO.__init__(self)

    # Look for journeys that cross midnight
    def find_journeys_crossing_midnight(self):
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
#        for journey, distance in self.nearby_locations[target_location].items():
#            walk_time = datetime.timedelta(minutes = dist/3200*30)
#            departure_datetime = target_arrival_datetime - walk_time
#            if location in adjacents:
#                curr_latest = adjacents[location]
#                if departure_datetime > curr_latest.when:
#                    adjacents[location] = ArrivePlaceTime(location, departure_datetime)
#            else:
#                adjacents[location] = ArrivePlaceTime(location, departure_datetime)
        return adjacents

    def _nearby_locations(self, target_location, target_arrival_datetime, adjacents):
        target_easting = self.location_details[target_location].additional.grid_reference_easting
        target_northing = self.location_details[target_location].additional.grid_reference_northing
        for location, data in self.location_details.items():
            easting = data.additional.grid_reference_easting
            northing = data.additional.grid_reference_northing
            dist = math.sqrt(((easting-target_easting)**2) + ((northing-target_northing)**2))
            if dist < self.walk_speed * self.walk_time: # 3600
                logging.debug("%s (%d,%d) is %d away from %s (%d,%d)" % (location, easting, northing, dist, target_location, target_easting, target_northing))
                walk_time = datetime.timedelta(seconds = dist / self.walk_speed)
                #walk_time = datetime.timedelta(minutes = dist/3200*30)
                departure_datetime = target_arrival_datetime - walk_time
                if location in adjacents:
                    curr_latest = adjacents[location]
                    if departure_datetime > curr_latest.when:
                        adjacents[location] = ArrivePlaceTime(location, departure_datetime)
                else:
                    adjacents[location] = ArrivePlaceTime(location, departure_datetime)

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
            if hop.location in adjacents:
                curr_latest = adjacents[hop.location]
                if departure_datetime > curr_latest.when:
                    adjacents[hop.location] = ArrivePlaceTime(hop.location, departure_datetime)
            else:
                adjacents[hop.location] = ArrivePlaceTime(hop.location, departure_datetime)
        
    def do_dijkstra(self, target_location, target_datetime, walk_speed=1, walk_time=3600):
        '''
        Run Dijkstra's algorithm to find latest departure time from all locations to
        arrive at the target location by the given time.

        target_location - station id to go to, e.g. 9100AYLSBRY or 210021422650
        target_datetime - when we want to arrive by
        '''

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
        queue = pqueue.PQueue()
        queue.insert(Priority(target_datetime), target_location)
        routes = {}
        routes[target_location] = [ ArrivePlaceTime(target_location, target_datetime) ] # how to get there
        self.final_destination = target_location
	self.walk_speed = walk_speed
	self.walk_time = walk_time

        while len(queue) > 0:
            # Find the item at top of queue
            (nearest_datetime, nearest_location) = queue.pop()
            nearest_datetime = nearest_datetime.when
            logging.info("taken " + nearest_location + " " + str(nearest_datetime) + " off queue")

            # That item is now settled
            settled[nearest_location] = nearest_datetime
            
            # Add all of its neighbours to the queue
            foundtimes = self.adjacent_location_times(nearest_location, nearest_datetime)
            for location, arrive_place_time in foundtimes.iteritems():
                when = arrive_place_time.when

                new_priority = Priority(when)
                try:
                    # See if this location is already in queue 
                    current_priority = queue[location]
                    # If we get here then it is, see if what we found is nearer and update priority
                    assert location not in settled
                    if new_priority < current_priority:
                        queue[location] = new_priority
                        routes[location] = routes[nearest_location] + [ arrive_place_time ]
                        logging.info("updated " + location + " from priority " + str(current_priority) + " to " + str(new_priority) + " in queue")
                except KeyError, e:
                    if location not in settled:
                        # No existing entry for location in queue
                        queue.insert(new_priority, location)
                        routes[location] = routes[nearest_location] + [ arrive_place_time ]
                        logging.info("added " + location + " " + str(new_priority) + " to queue")

        return (settled, routes)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
