#
# makeplan.py:
# Make maps of journey times from NPTDR public transport route data.
#
# Copyright (c) 2008 UK Citizens Online Democracy. All rights reserved.
# Email: francis@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: makeplan.py,v 1.3 2009-02-09 11:51:26 francis Exp $
#

import logging
import pqueue
import datetime

import mysociety.atcocif

class PlanningATCO(mysociety.atcocif.ATCO):
    # train_interchange_default - time in minutes to allow by default to change trains at same station
    # bus_interchange_default - likewise for buses, at exact same stop
    def __init__(self, train_interchange_default = 5, bus_interchange_default = 1):
        self.train_interchange_default = train_interchange_default
        self.bus_interchange_default = bus_interchange_default
        mysociety.atcocif.ATCO.__init__(self)

    # Make dictionaries so it is quick to look up all journeys visiting a particular location etc.
    def index_by_short_codes(self):
        self.journeys_visiting_location = {}
        for journey in self.journeys:
            for hop in journey.hops:
                if hop.location not in self.journeys_visiting_location:
                    self.journeys_visiting_location[hop.location] = set()

                if journey in self.journeys_visiting_location[hop.location]:
                    if hop == journey.hops[0] and hop == journey.hops[-1]:
                        # if it's a simple loop, starting and ending at same point, then that's OK
                        logging.debug("journey " + journey.unique_journey_identifier + " loops")
                        pass
                    else:
                        assert "same location %s appears twice in one journey %s, and not at start/end" % (hop.location, journey.unique_journey_identifier)

                self.journeys_visiting_location[hop.location].add(journey)

        self.location_details = {}
        for location in self.locations:
            self.location_details[location.location] = location

    # Look for journeys that cross midnight
    def find_journeys_crossing_midnight(self):
        for journey in self.journeys:
            previous_departure_time = datetime.time(0, 0, 0)
            for hop in journey.hops:
                if hop.is_pick_up():
                    if previous_departure_time > hop.published_departure_time:
                        print "journey " + journey.unique_journey_identifier + " spans midnight"
                    previous_departure_time = hop.published_departure_time
 
    # Adjacency function for use with Dijkstra's algorithm on earliest time to arrive somewhere.
    # Given a location (string short code) and a date/time, it finds every
    # other station you can get there on time by one direct train/bus. 
    def adjacent_location_times(self, target_location, target_arrival_datetime):
        # Check that there are journeys visiting this location
        logging.debug("adjacent_location_times target_location: " + target_location + " target_arrival_datetime: " + str(target_arrival_datetime))
        if target_location not in self.journeys_visiting_location:
            raise Exception, "No journeys known visiting target_location " + target_location

        # Adjacents is dictionary from location to time at that location, and
        # is the data structure we are going to return from this function.
        adjacents = {}
        # Go through every journey visiting the location
        for journey in self.journeys_visiting_location[target_location]:
            logging.debug("\tconsidering journey: " + journey.unique_journey_identifier)

            self._adjacent_location_times_for_journey(target_location, target_arrival_datetime, adjacents, journey)

        return adjacents

    def _adjacent_location_times_for_journey(self, target_location, target_arrival_datetime, adjacents, journey):
        # Check whether the journey runs on the relevant date
        # XXX assumes we don't do journeys over midnight
        (valid_on_date, reason) = journey.is_valid_on_date(target_arrival_datetime.date()) 
        if not valid_on_date:
            logging.debug("\t\tnot valid on date: " + reason)
        else:
            # Find out when it arrives at this stop
            arrival_time_at_target_location = journey.find_arrival_time_at_location(target_location)
            if arrival_time_at_target_location == None:
                # arrival_time_at_target_location could be None here for e.g. pick up only stops
                pass
            else:
                logging.debug("\t\tarrival time at target location: " + str(arrival_time_at_target_location))
                arrival_datetime_at_target_location = datetime.datetime.combine(target_arrival_datetime.date(), arrival_time_at_target_location)

                # Work out how long we need to allow to change at the stop
                # XXX here need to know if the stop is the last destination stop, as you don't need interchange time
                if journey.vehicle_type == 'TRAIN':
                    interchange_time_in_minutes = self.train_interchange_default
                else:
                    interchange_time_in_minutes = self.bus_interchange_default
                interchange_time = datetime.timedelta(minutes = interchange_time_in_minutes)
                
                # See whether if we want to use this journey to get to this
                # stop, we get there on time to change to the next journey.
                if arrival_datetime_at_target_location + interchange_time > target_arrival_datetime:
                    logging.debug("\t\twhich is too late with interchange time %s, so not using journey" % str(interchange_time))
                else:
                    logging.debug("\t\tadding stops")
                    self._adjacent_location_times_add_stops(target_location, target_arrival_datetime, adjacents, journey, arrival_datetime_at_target_location)

    def _adjacent_location_times_add_stops(self, target_location, target_arrival_datetime, adjacents, journey, arrival_datetime_at_target_location):
        # Now go through every earlier stop, and add it to the list of returnable nodes
        for hop in journey.hops:
            # We've arrived at the target location (check is_set_down here so looped
            # journeys, where we end on stop we started, work)
            if hop.is_set_down() and hop.location == target_location:
                break
            if hop.is_pick_up():
                departure_datetime = datetime.datetime.combine(target_arrival_datetime.date(), hop.published_departure_time)
                # if the time at this hop is later than at target, must be a midnight rollover, and really
                # this hop is on the the day before, so change to that
                # XXX bah this is rubbish as it won't have done the is right day check right
                if departure_datetime > arrival_datetime_at_target_location:
                    departure_datetime = datetime.datetime.combine(target_arrival_datetime.date() - datetime.timedelta(1), hop.published_departure_time)
                # Use this location if new, or if it is later departure time than any previous one the same we've found.
                if hop.location in adjacents:
                    curr_latest = adjacents[hop.location]
                    if departure_datetime > curr_latest:
                        adjacents[hop.location] = departure_datetime
                else:
                    adjacents[hop.location] = departure_datetime
            
    def do_dijkstra(self, target_location, target_datetime):
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
                return "Priority '" + str(self.when) + "'"
        
        # Set up initial state
        settled = {} # dictionary from location to datetime
        queue = pqueue.PQueue()
        queue.insert(Priority(target_datetime), target_location)
        routes = {}
        routes[target_location] = [ (target_location, target_datetime) ] # how to get there

        while len(queue) > 0:
            # Find the item at top of queue
            (nearest_datetime, nearest_location) = queue.pop()
            nearest_datetime = nearest_datetime.when
            logging.info("taken " + nearest_location + " " + str(nearest_datetime) + " off queue")

            # That item is now settled
            settled[nearest_location] = nearest_datetime
            
            # Add all of its neighbours to the queue
            foundtimes = self.adjacent_location_times(nearest_location, nearest_datetime)
            for location, when in foundtimes.iteritems():
                new_priority = Priority(when)
                try:
                    # See if this location is already in queue 
                    current_priority = queue[location]
                    # If we get here then it is, see if what we found is nearer and update priority
                    assert location not in settled
                    if new_priority < current_priority:
                        queue[location] = new_priority
                        routes[location] = routes[nearest_location] + [ (location, when) ]
                        logging.info("updated " + location + " from priority " + str(current_priority) + " to " + str(new_priority) + " in queue")
                except KeyError, e:
                    if location not in settled:
                        # No existing entry for location in queue
                        queue.insert(new_priority, location)
                        routes[location] = routes[nearest_location] + [ (location, when) ]
                        logging.info("added " + location + " " + str(new_priority) + " to queue")

        return (settled, routes)


