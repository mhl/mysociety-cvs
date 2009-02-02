#
# makeplan.py:
# Make maps of journey times from NPTDR public transport route data.
#
# Copyright (c) 2008 UK Citizens Online Democracy. All rights reserved.
# Email: francis@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: makeplan.py,v 1.1 2009-02-02 16:01:30 francis Exp $
#

import logging
import pqueue

def do_dijkstra(atco, target_location, target_datetime):
    '''
    Run Dijkstra's algorithm to find latest departure time from all locations to
    arrive at the target location by the given time.

    atco - data structure containing ATCO file, loaded by mysociety.atcocif.ATCO()
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
        foundtimes = atco.adjacent_location_times(nearest_location, nearest_datetime)
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


