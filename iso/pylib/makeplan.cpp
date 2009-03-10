//
// makeplan.cpp:
// Make maps of journey times from NPTDR public transport route data.
// Reads input files from makefast.py.
//
// Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
// Email: francis@mysociety.org; WWW: http://www.mysociety.org/
//
// $Id: makeplan.cpp,v 1.2 2009-03-10 22:28:28 francis Exp $
//

#include <set>
#include <map>
#include <vector>
#include <string>
#include <cstdio>

#include <boost/format.hpp>
#include <boost/foreach.hpp>

#include <stdio.h>
#include <stdarg.h>
#include <assert.h>

typedef short Minutes; // after midnight

typedef int LocationID;
class Location {
    public:
    std::string text_id; // e.g. 9100BANGOR
    int easting; // OS grid coordinate
    int northing; // OS grid coordinate

    std::string toString() const {
        return (boost::format("Location(%s E:%d N:%d)") % this->text_id % this->easting % this->northing).str();
    }
};

class Hop {
    public:
    LocationID location_id;
    Minutes mins_arr; // minutes after midnight of arrival, or -1 if not set down stop
    Minutes mins_dep; // minutes after midnight of departure, or -1 if not pick up stop

    std::string toString() const {
        return (boost::format("Hop(loc:%s arr:%d dep:%d)") % this->location_id % this->mins_arr % this->mins_dep).str();
    }
};

typedef int JourneyID;
class Journey {
    public:
    std::string text_id; // e.g. CH-E7AB
    std::vector<Hop> hops;
    char vehicle_type; // T = train, B = bus

    std::string toString() const {
        return (boost::format("Journey(%s)") % this->text_id).str();
    }
};

class ArrivePlaceTime {
    /* Stores a location and date/time of arrival (including interchange wait)
    at that location. */

    public:

    LocationID location_id;
    Minutes when; // minutes after midnight

    ArrivePlaceTime(LocationID l_location_id, Minutes l_when) {
        this->location_id = l_location_id;
        this->when = l_when;
    }

    ArrivePlaceTime() {
        this->location_id = -1;
        this->when = -1;
    }

    std::string repr() const {
        std::string ret;
        //ret = "ArrivePlaceTime(" + this->location_id + ", " + this->when + ")";
        ret = "ArrivePlaceTime(...)";
        return ret;
    }
};

/* Map from a location, to the best time/location to leave that place */
typedef std::map<LocationID, ArrivePlaceTime> Adjacents;

/* Logging */
int log(const char* fmt, ...) {
    va_list ap;
    va_start(ap, fmt);
    vprintf(fmt, ap);
    va_end(ap);
    printf("\n");
}


/* Most similar to Python's Exception */
class Exception : public std::exception
{
    std::string s;
public:
    Exception(std::string s_) : s("Exception: " + s_) { }
    ~Exception() throw() { }
    const char* what() const throw() { return s.c_str(); }
};

/* Loads and represents a set of ATCO-CIF files, and can generate large
sets of quickest routes from them.
*/
class PlanningATCO {
    public: 

    int train_interchange_default;
    int bus_interchange_default;
    int number_of_locations;
    int number_of_journeys;

    std::vector<Location> locations;
    std::vector<Journey> journeys;

    typedef std::map<LocationID, std::set<JourneyID> > JourneysVisitingLocation;
    JourneysVisitingLocation journeys_visiting_location;

    LocationID final_destination_id;

    /* Create object that generates shortest journey times for all stations
    in a public transport network defined by an ATCO-CIF timetable file.

    train_interchange_default - time in minutes to allow by default to change trains at same station
    bus_interchange_default - likewise for buses, at exact same stop
    */
    PlanningATCO(int l_train_interchange_default = 5, int l_bus_interchange_default = 1) {
        this->train_interchange_default = l_train_interchange_default;
        this->bus_interchange_default = l_bus_interchange_default;
    }

    /* Loads a string which has a byte lenth prefix */
    std::string _read_pascal_string(FILE *fp) {
        short len;
        fread(&len, 1, sizeof(short), fp);
        std::string ret;
        ret.resize(len);
        fread(&ret[0], 1, len, fp);
        return ret;
    }

    /* Read in binary timetable files, exported by makefast.py */
    void load_binary_timetable(const std::string& l_in_prefix) {
        // Load in locations
        std::string location_filename = l_in_prefix + ".locations";
        FILE *fp = fopen(location_filename.c_str(), "rb");
        fread(&this->number_of_locations, 1, sizeof(int), fp);
        log("number of locations %d", this->number_of_locations);

        locations.resize(this->number_of_locations + 1);
        for (int i = 1; i <= this->number_of_locations; ++i) {
            LocationID id;
            fread(&id, 1, sizeof(LocationID), fp);
            assert(int(id) == i);

            Location *l = &this->locations[i];
            l->text_id = this->_read_pascal_string(fp);

            fread(&l->easting, 1, sizeof(l->easting), fp);
            fread(&l->northing, 1, sizeof(l->northing), fp);

            log("loaded location: %s", l->toString().c_str());
        }

        fclose(fp);

        // Load in journeys
        std::string journey_filename = l_in_prefix + ".journeys";
        fp = fopen(journey_filename.c_str(), "rb");
        fread(&this->number_of_journeys, 1, sizeof(int), fp);
        log("number of journeys %d", this->number_of_journeys);

        journeys.resize(this->number_of_journeys + 1);
        for (int i = 1; i <= this->number_of_journeys; ++i) {
            JourneyID id;
            fread(&id, 1, sizeof(JourneyID), fp);
            assert(int(id) == i);

            Journey *j = &this->journeys[i];
            j->text_id = this->_read_pascal_string(fp);

            fread(&j->vehicle_type, 1, sizeof(char), fp);

            short number_of_hops;
            fread(&number_of_hops, 1, sizeof(number_of_hops), fp);
            log("loaded journey: %s hops:%d", j->toString().c_str(), number_of_hops);

            j->hops.resize(number_of_hops);
            for (int ii = 0; ii < number_of_hops; ++ii) {
                Hop hop;
                fread(&hop.location_id, 1, sizeof(hop.location_id), fp);
                fread(&hop.mins_arr, 1, sizeof(hop.mins_arr), fp);
                fread(&hop.mins_dep, 1, sizeof(hop.mins_dep), fp);
                j->hops[ii] = hop;
                log("loaded hop: %s", hop.toString().c_str());

                // update index
                journeys_visiting_location[hop.location_id].insert(id);
            }

        }

    }

    /* Adjacency function for use with Dijkstra's algorithm on earliest
    time to arrive somewhere.  Given a location and a date/time, it finds every
    other station from which you can get there on time by one *direct*
    train/bus. 

    Adjacents is map from location to time at that location, and
    is the data structure we are going to return from this function.
    */
    void adjacent_location_times(Adjacents &adjacents, LocationID target_location_id, Minutes target_arrival_time) {
        // Check that there are journeys visiting this location
        log("adjacent_location_times target_location: %d target_arrival_time: %d", target_location_id, target_arrival_time);
        JourneysVisitingLocation::iterator it = this->journeys_visiting_location.find(target_location_id);
        if (it == journeys_visiting_location.end()) {
            throw Exception((boost::format("No journeys known visiting target_location id %d") % target_location_id).str());
        }

        // Go through every journey visiting the location
        std::set<JourneyID> journey_list = it->second;
        BOOST_FOREACH(JourneyID journey_id, journey_list) {
            this->_adjacent_location_times_for_journey(target_location_id, target_arrival_time, adjacents, journey_id);
        }
        /*
        // self._nearby_locations(target_location, target_arrival_datetime, adjacents)
        // */
    }

    /* Private helper function. Store a time we can leave a station, if it
    is later than previous direct routes we have for leaving from that
    station and arriving at target. */
    void _add_to_adjacents(const ArrivePlaceTime &arrive_place_time, Adjacents &adjacents) {
        if (adjacents.find(arrive_place_time.location_id) != adjacents.end()) {
            ArrivePlaceTime curr_latest = adjacents[arrive_place_time.location_id];
            if (arrive_place_time.when > curr_latest.when) {
                adjacents[arrive_place_time.location_id] = arrive_place_time;
            }
        } else {
            adjacents[arrive_place_time.location_id] = arrive_place_time;
        }
    }

/*
    def _nearby_locations(Location target_location_id, const Minutes& target_arrival_time, Adjacents& adjacents):
        '''Private function, called by adjacent_location_times. Looks for
        stations you can walk from to get to the target station.  This is
        constrained by self.walk_speed and self.walk_time. Adds any such
        stations to the adjacents structure.
        '''

        try:
            target_easting = self.location_from_id[target_location].additional.grid_reference_easting
            target_northing = self.location_from_id[target_location].additional.grid_reference_northing
        except AttributeError, e:
            return

        for location, dist in self.nearby_locations[self.location_from_id[target_location]].iteritems():
            logging.debug("%s (%d,%d) is %d away from %s (%d,%d)" % (location, location.additional.grid_reference_easting, location.additional.grid_reference_northing, dist, target_location, target_easting, target_northing))
            walk_time = datetime.timedelta(seconds = dist / self.walk_speed)
            walk_departure_datetime = target_arrival_datetime - walk_time
            arrive_time_place = ArrivePlaceTime(location.location, walk_departure_datetime, onwards_leg_type = 'walk', onwards_walk_time = walk_time)
            // Use this location if new, or if it is later departure time than any previous one the same we've found.
            self._add_to_adjacents(arrive_time_place, adjacents)
*/

    // How long after a journey it takes to interchange to catch another form of
    // transport at the destination stop.
    Minutes _interchange_time_after_journey(JourneyID journey_id) {
        Journey& journey = this->journeys[journey_id];

        if (journey.vehicle_type == 'T') {
            return this->train_interchange_default;
        } else {  // Bus, Air, Metro/Tram, Ferry/River Bus XXX
            return this->bus_interchange_default;
        }
    }

    /* Private function, called by adjacent_location_times. Finds every
    other station you can get to the destination on time, using
    the specific given bus/train in journey. Results are stored in the
    adjacents structure.
    */
    void _adjacent_location_times_for_journey(const LocationID target_location_id, const Minutes target_arrival_time, Adjacents& adjacents, const JourneyID journey_id) {
        // All journeys run on the valid date; the check is done in the Python binary exporter.
        Journey& journey = this->journeys[journey_id];

        // Work out how long we need to allow to change at the stop
        Minutes interchange_time;
        if (target_location_id == this->final_destination_id) {
            interchange_time = 0;
        } else {
            interchange_time = this->_interchange_time_after_journey(journey_id);
        }
        
        // Pick the latest of arrival times that's before the time we're
        // currently at (plus interchange time of course). Usually there'll
        // only be one of arrival time to check, but there can be more for
        // looped journeys.
        Minutes arrival_time_at_target_location = -1;
        BOOST_FOREACH(Hop hop, journey.hops) {
            // Find hops that arrive at the target
            if (hop.location_id == target_location_id) {
                Minutes possible_arrival_time_at_target_location = hop.mins_arr;
                if (hop.mins_arr == -1) {
                    continue;
                }
                // See if that is a closer arrival time than what we got so far
                assert(hop.mins_arr >= 0);
                if (possible_arrival_time_at_target_location + interchange_time <= target_arrival_time 
                    && (arrival_time_at_target_location == -1 || arrival_time_at_target_location < possible_arrival_time_at_target_location)) {
                    arrival_time_at_target_location = possible_arrival_time_at_target_location;
                }
            }
        }

        // See whether if we want to use this journey to get to this
        // stop, we get there on time to change to the next journey.
        if (arrival_time_at_target_location == -1) {
            log("\t\twhich are all too late with interchange time %d, so not using journey", interchange_time);
            return;
        }

        log("\t\tadding stops");
        // self._adjacent_location_times_add_stops(target_location, target_arrival_datetime, adjacents, journey, arrival_datetime_at_target_location)
    }
}; /*

    '''Private function, called by _adjacent_location_times_for_journey.
    For a given journey, adds individual stops which are valid to the
    adjacents structure.
    '''
    void _adjacent_location_times_add_stops(self, target_location, target_arrival_datetime, adjacents, journey, arrival_datetime_at_target_location) {

        // Now go through every earlier stop, and add it to the list of returnable nodes
        for hop in journey.hops:
            // Ignore the target location
            if hop.location == target_location:
                continue

            // If the stop doesn't pick up passengers, don't use it
            if not hop.is_pick_up():
                continue

            departure_datetime = datetime.datetime.combine(target_arrival_datetime.date(), hop.published_departure_time)

            // If the time at this hop is later than at target, we stop.
            // We use time for this, rather than stopping at the target location,
            // so we cope with looped journeys.
            // XXX This will also stop midnight rollover journeys at midnight.
            // If we care about maps near midnight, then this needs fixing by
            // duplicating the journey at an earlier stage in processing, as
            // well as by working out the right date/time in
            // _adjacent_location_times_for_journey to get is_valid_on_date
            // right.
            if departure_datetime > arrival_datetime_at_target_location:
                break

            // Use this location if new, or if it is later departure time than any previous one the same we've found.
            arrive_place_time = ArrivePlaceTime(hop.location, departure_datetime, onwards_leg_type = 'journey', onwards_journey = journey)
            self._add_to_adjacents(arrive_place_time, adjacents)
    }

    '''
    Run Dijkstra's algorithm to find latest departure time from all locations to
    arrive at the target location by the given time.

    target_location - station id to go to, e.g. 9100AYLSBRY or 210021422650
    target_datetime - when we want to arrive by
    '''
    void do_dijkstra(self, target_location, target_datetime, walk_speed=1, walk_time=3600, earliest_departure=None) {
        // The thing we're going to use for priority in the pqueue
        class Priority:
            def __init__(self, when):
                self.when = when
            // operator just for use on priority queue
            def __cmp__(self, other):
                // The priority queue pops smallest first, whereas we want
                // largest, so these are reversed from expected direction
                if self.when < other.when:
                    return 1
                if self.when == other.when:
                    return 0 
                if self.when > other.when:
                    return -1
                assert False
            def __repr__(self):
                return "Priority(" + repr(self.when) + ")"

       
        // Set up initial state
        settled = {} // dictionary from location to datetime
        settled_routes = {} // routes of settled journeys
        queue = pqueue.PQueue()
        queue.insert(Priority(target_datetime), target_location)
        routes = {}
        routes[target_location] = [ ArrivePlaceTime(target_location, target_datetime, onwards_leg_type = 'already_there') ] // how to get there
        self.final_destination = target_location
        self.walk_speed = walk_speed
        self.walk_time = walk_time

        while len(queue) > 0:
            // Find the item at top of queue
            (nearest_datetime, nearest_location) = queue.pop()
            nearest_datetime = nearest_datetime.when

            // If it is earlier than earliest departure we are going back to, then finish
            if earliest_departure and nearest_datetime < earliest_departure:
                break

            // That item is now settled
            settled[nearest_location] = nearest_datetime
            // ... copy the route into settled_routes, so we only return routes
            // we know we finished (rather than the partial, best-so-far that is
            // in routes)
            settled_routes[nearest_location] = routes[nearest_location]
            logging.info("settled " + nearest_location + " " + str(nearest_datetime))
            
            // Add all of its neighbours to the queue
            foundtimes = self.adjacent_location_times(nearest_location, nearest_datetime)
            for location, arrive_place_time in foundtimes.iteritems():
                new_priority = Priority(arrive_place_time.when)
                try:
                    // See if this location is already in queue 
                    current_priority = queue[location]
                    // If we get here then it is, see if what we found is nearer and update priority
                    assert location not in settled
                    if new_priority < current_priority:
                        queue[location] = new_priority
                        routes[location] = [ arrive_place_time ] + routes[nearest_location] 
                        logging.debug("updated " + location + " from priority " + str(current_priority) + " to " + str(new_priority) + " in queue")
                except KeyError, e: // only way of testing presence in queue is to catch an exception
                    if location not in settled:
                        // No existing entry for location in queue
                        queue.insert(new_priority, location)
                        routes[location] = [ arrive_place_time ] + routes[nearest_location] 
                        logging.debug("added " + location + " " + str(new_priority) + " to queue")

        return (settled, settled_routes)
    }

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
                    print "    Leave by walking to %s, will take %.02f mins" % (next_stop.location, stop.onwards_walk_time.seconds / 60.0)
                elif stop.onwards_leg_type == 'journey':
                    departure_times = stop.onwards_journey.find_departure_times_at_location(stop.location)
                    departure_time = []
                    for a in departure_times:
                        departure_time.append(a.strftime("%H:%M:%S"))
                    arrival_times = stop.onwards_journey.find_arrival_times_at_location(next_stop.location)
                    arrival_time = []
                    for a in arrival_times:
                        arrival_time.append(a.strftime("%H:%M:%S"))
                    print "    Leave " + stop.location + " by " + stop.onwards_journey.vehicle_type + " on the " + ','.join(departure_time) + ", arriving " + next_stop.location + " at " + ','.join(arrival_time)
                else:
                    raise "Unknown leg type '" + stop.onwards_leg_type + "'"

*/

int main() {
    printf("running makeplan.cpp\n");
    PlanningATCO atco;
    atco.load_binary_timetable("/home/francis/toobig/nptdr/gen/nptdr-B32QD-40000.fastindex");
    return 0;
};


