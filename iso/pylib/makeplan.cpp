//
// makeplan.cpp:
// Make maps of journey times from NPTDR public transport route data.
// Reads input files from makefast.py.
//
// Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
// Email: francis@mysociety.org; WWW: http://www.mysociety.org/
//
// $Id: makeplan.cpp,v 1.10 2009-03-12 03:41:38 francis Exp $
//

// Usage:
// g++ -g makeplan.cpp -DDEBUG
// ./a.out /home/francis/toobig/nptdr/gen/nptdr-B32QD-40000 540 9100BHAMSNH
//
// Is quicker without logging that DEBUG causes.

#include <set>
#include <map>
#include <vector>
#include <list>
#include <string>
#include <cstdio>
#include <fstream>

#include <boost/format.hpp>
#include <boost/foreach.hpp>
#include <boost/pending/relaxed_heap.hpp>

#include <stdio.h>
#include <stdarg.h>
#include <assert.h>
#include <math.h>
#include <time.h>

typedef short Minutes; // after midnight

// Stuff for relaxed_heap for Dijkstra's algorithm
// XXX must be global, is there a way to use relaxed_heap and this not be?
// Otherwise this whole thing can't be called from two threads using same data,
// which is a pain.
typedef std::vector<boost::optional<Minutes> > QueueValuesType;
QueueValuesType queue_values;
struct LessValues
{
    bool operator()(unsigned x, unsigned y) const
    {
        assert(queue_values[x] && queue_values[y]);
        return queue_values[x] > queue_values[y];
    }
};

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

    bool is_pick_up() {
        return mins_dep != -1;
    }
    bool is_set_down() {
        return mins_arr != -1;
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
typedef std::pair<LocationID, ArrivePlaceTime> AdjacentsPair;

/* Result types from Dijkstra's algorithm */
typedef std::map<LocationID, Minutes> Settled;
typedef std::pair<LocationID, Minutes> SettledPair;
typedef std::map<LocationID, std::list<ArrivePlaceTime> > Routes;
typedef std::pair<LocationID, std::list<ArrivePlaceTime> > RoutesPair;

/* Logging */
void do_log(boost::basic_format<char, std::char_traits<char>, std::allocator<char> > &bf) {
    puts(bf.str().c_str());
}
void do_log(const std::string& str) {
    puts(str.c_str());
}
#ifdef DEBUG
    #define log(message) do_log(message);
#else
    #define log(message) while(0) { };
#endif

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

    float walk_speed; // metres /s ec
    float walk_time; // secs

    std::vector<Location> locations;
    std::vector<Journey> journeys;

    std::map<std::string, LocationID> locations_by_text_id;

    typedef std::map<LocationID, std::set<JourneyID> > JourneysVisitingLocation;
    JourneysVisitingLocation journeys_visiting_location;

    typedef std::map<LocationID, float> NearbyLocationsInner;
    typedef std::map<LocationID, NearbyLocationsInner> NearbyLocations;
    typedef std::pair<LocationID, double> NearbyLocationsInnerPair;
    NearbyLocations nearby_locations;

    LocationID final_destination_id;

    /* Create object that generates shortest journey times for all stations
    in a public transport network defined by an ATCO-CIF timetable file.

    train_interchange_default - time in minutes to allow by default to change trains at same station
    bus_interchange_default - likewise for buses, at exact same stop
    */
    PlanningATCO(int l_train_interchange_default = 5, int l_bus_interchange_default = 1, float l_walk_speed=1.0, float l_walk_time=300.0 
    ) {
        this->train_interchange_default = l_train_interchange_default;
        this->bus_interchange_default = l_bus_interchange_default;
        this->walk_speed = l_walk_speed;
        this->walk_time = l_walk_time;
    }

    /* Loads a string which has a byte lenth prefix */
    std::string _read_pascal_string(FILE *fp) {
        short len;
        fread(&len, 1, sizeof(short), fp);
        // log(boost::format("_read_pascal_string len: %d") % len);
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
        if (!fp) {
            printf("Failed to open index file: %s\n", location_filename.c_str());
            exit(1);
        }
        fread(&this->number_of_locations, 1, sizeof(int), fp);
        log(boost::format("number of locations: %d") % this->number_of_locations);

        locations.resize(this->number_of_locations + 1);
        for (int i = 1; i <= this->number_of_locations; ++i) {
            LocationID id;
            fread(&id, 1, sizeof(LocationID), fp);
            assert(int(id) == i);

            Location *l = &this->locations[i];
            l->text_id = this->_read_pascal_string(fp);

            fread(&l->easting, 1, sizeof(l->easting), fp);
            fread(&l->northing, 1, sizeof(l->northing), fp);

            locations_by_text_id[l->text_id] = id;

            log(boost::format("loaded location: %s") % l->toString().c_str());
        }

        fclose(fp);

        // Load in journeys
        std::string journey_filename = l_in_prefix + ".journeys";
        fp = fopen(journey_filename.c_str(), "rb");
        if (!fp) {
            printf("Failed to open index file: %s\n", journey_filename.c_str());
            exit(1);
        }
        fread(&this->number_of_journeys, 1, sizeof(int), fp);
        log(boost::format("number of journeys: %d") % this->number_of_journeys);

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
            log(boost::format("loaded journey: %s hops:%d") % j->toString().c_str() % number_of_hops);

            j->hops.resize(number_of_hops);
            for (int ii = 0; ii < number_of_hops; ++ii) {
                Hop hop;
                fread(&hop.location_id, 1, sizeof(hop.location_id), fp);
                fread(&hop.mins_arr, 1, sizeof(hop.mins_arr), fp);
                fread(&hop.mins_dep, 1, sizeof(hop.mins_dep), fp);
                j->hops[ii] = hop;
                log(boost::format("loaded hop: %s") % hop.toString().c_str());

                // update index
                journeys_visiting_location[hop.location_id].insert(id);
            }
        }

        // Proximity index
        double nearby_max_distance = double(this->walk_speed) * double(this->walk_time);
        double nearby_max_distance_sq = nearby_max_distance * nearby_max_distance;

        this->nearby_locations.clear();
        for (LocationID location_id = 1; location_id <= this->number_of_locations; location_id++) {
            Location *location = &this->locations[location_id];
            double easting = location->easting;
            double northing = location->northing;
            for (LocationID other_location_id = location_id + 1; other_location_id <= this->number_of_locations; other_location_id++) {
                Location *other_location = &this->locations[other_location_id];
                double other_easting = other_location->easting;
                double other_northing = other_location->northing;
                double sqdist = (easting - other_easting)*(easting - other_easting)
                              + (northing - other_northing)*(northing - other_northing);

                if (sqdist < nearby_max_distance_sq) {
                    double dist = sqrt(sqdist);
                    log(boost::format("load_binary_timetable: %s (%d,%d) is %f (sq %f, max %f) away from %s (%d,%d)") % location->text_id % easting % northing % dist % sqdist % nearby_max_distance % other_location->text_id % other_easting % other_northing);
                    nearby_locations[location_id][other_location_id] = dist;
                    nearby_locations[other_location_id][location_id] = dist;
                }
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
        log(boost::format("adjacent_location_times target_location: %s target_arrival_time: %d") % this->locations[target_location_id].text_id % target_arrival_time);
        JourneysVisitingLocation::iterator it = this->journeys_visiting_location.find(target_location_id);
        if (it == journeys_visiting_location.end()) {
            // This can happen, for example, with locations that are only
            // stopped at at the weekend, when it is a weekday. The fastplan.py
            // code doesn't strip such cases.
            return;
        }

        // Go through every journey visiting the location
        std::set<JourneyID> journey_list = it->second;
        BOOST_FOREACH(JourneyID journey_id, journey_list) {
            log(boost::format("\tconsidering journey: %s") % this->journeys[journey_id].text_id)
            this->_adjacent_location_times_for_journey(target_location_id, target_arrival_time, adjacents, journey_id);
        }
        this->_nearby_locations(target_location_id, target_arrival_time, adjacents);
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

    /* How long it takes to walk between two stations dist distance apart.
    */
    Minutes _walk_time_apart(float dist) {
        float sec = float(dist) / float(this->walk_speed);
        // round up to nearest minute
        Minutes walk_time = int((sec + 59) / 60);
        return walk_time;
    }


    void _nearby_locations(LocationID target_location_id, const Minutes& target_arrival_time, Adjacents& adjacents) {
        /* Private function, called by adjacent_location_times. Looks for
        stations you can walk from to get to the target station.  This is
        constrained by self.walk_speed and self.walk_time. Adds any such
        stations to the adjacents structure.
        */
        Location *target_location = &this->locations[target_location_id];

        int target_easting = this->locations[target_location_id].easting;
        int target_northing = this->locations[target_location_id].northing;

        NearbyLocationsInner &nearby_locations_inner = this->nearby_locations[target_location_id];
        BOOST_FOREACH(NearbyLocationsInnerPair p, nearby_locations_inner) {
            LocationID location_id = p.first;
            double dist = p.second;

            Location *location = &this->locations[location_id];

            log(boost::format("_nearby_locations: %s (%d,%d) is %d away from %s (%d,%d)") % location->text_id % location->easting % location->northing % dist % target_location->text_id % target_easting % target_northing)

            Minutes walk_time = this->_walk_time_apart(dist);
            Minutes walk_departure_time = target_arrival_time - walk_time;
            ArrivePlaceTime arrive_time_place(location_id, walk_departure_time /*, onwards_leg_type = 'walk', onwards_walk_time = walk_time */);
            // Use this location if new, or if it is later departure time than any previous one the same we've found.
            this->_add_to_adjacents(arrive_time_place, adjacents);
        }
    }

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
        Journey& journey = this->journeys[journey_id];

        // All journeys run on the valid date; the check is done in the Python binary exporter.

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
            if (hop.location_id != target_location_id) {
                continue;
            }
            if (!hop.is_set_down()) {
                continue;
            }
            Minutes possible_arrival_time_at_target_location = hop.mins_arr;
            log(boost::format("\t\tarrival time %d at target location %s") % possible_arrival_time_at_target_location % this->locations[target_location_id].text_id);
            // See if that is a closer arrival time than what we got so far
            assert(hop.mins_arr >= 0);
            if (possible_arrival_time_at_target_location + interchange_time <= target_arrival_time 
                && (arrival_time_at_target_location == -1 || arrival_time_at_target_location < possible_arrival_time_at_target_location)) {
                arrival_time_at_target_location = possible_arrival_time_at_target_location;
            }
        }

        // See whether if we want to use this journey to get to this
        // stop, we get there on time to change to the next journey.
        if (arrival_time_at_target_location == -1) {
            log(boost::format("\t\twhich are all too late for %s by %d with interchange time %d so not using journey") % this->locations[target_location_id].text_id % target_arrival_time % interchange_time);
            return;
        }

        log("\t\tadding stops");
        this->_adjacent_location_times_add_stops(target_location_id, target_arrival_time, adjacents, journey_id, arrival_time_at_target_location);
    }

    /* Private function, called by _adjacent_location_times_for_journey.
    For a given journey, adds individual stops which are valid to the
    adjacents structure.
    */
    void _adjacent_location_times_add_stops(const LocationID target_location_id, const Minutes target_arrival_time, Adjacents &adjacents, const JourneyID journey_id, const Minutes arrival_time_at_target_location) {
        Journey& journey = this->journeys[journey_id];

        // Now go through every earlier stop, and add it to the list of returnable nodes
        BOOST_FOREACH(Hop hop, journey.hops) {
            // Ignore the target location
            if (hop.location_id == target_location_id) {
                continue;
            }

            // If the stop doesn't pick up passengers, don't use it
            if (!hop.is_pick_up()) {
                continue;
            }

            Minutes departure_time = hop.mins_dep;

            // If the time at this hop is later than at target, we stop.
            // We use time for this, rather than stopping at the target location,
            // so we cope with looped journeys.
            // XXX This will also stop midnight rollover journeys at midnight.
            // If we care about maps near midnight, then this needs fixing by
            // duplicating the journey at an earlier stage in processing, as
            // well as by working out the right date/time in
            // _adjacent_location_times_for_journey to get is_valid_on_date
            // right.
            if (departure_time > arrival_time_at_target_location) {
                break;
            }

            // Use this location if new, or if it is later departure time than any previous one the same we've found.
            ArrivePlaceTime arrive_place_time(hop.location_id, departure_time /*, onwards_leg_type = 'journey', onwards_journey = journey*/);
            this->_add_to_adjacents(arrive_place_time, adjacents);
        }
    }

    /*
    Run Dijkstra's algorithm to find latest departure time from all locations to
    arrive at the target location by the given time.

    target_location - station id to go to, e.g. 9100AYLSBRY or 210021422650
    target_datetime - when we want to arrive by
    */
    void do_dijkstra(Settled& settled, Routes& settled_routes, const LocationID target_location_id, const Minutes target_time /*, earliest_departure=None*/) {
        /* Try out heaps
        int max_values = 100;
        queue_values.resize(max_values);
        boost::relaxed_heap<unsigned, LessValues> heap(max_values);

        queue_values[9] = 1000;
        heap.push(9);
        queue_values[8] = 2000;
        heap.push(8);
        queue_values[7] = 1500;
        heap.push(7);
        queue_values[6] = 1300;
        heap.push(6);
        queue_values[5] = 1900;
        heap.push(5);

        int victim;
        Minutes m;

        victim = heap.top();
        m = *queue_values[victim];
        log("minutes: %d location: %d", m, victim);

        queue_values[7] = 5000;
        heap.update(7);

        victim = heap.top();
        m = *queue_values[victim];
        log("minutes: %d location: %d", m, victim);
        */
        
        Routes routes; // how to get there
        routes[target_location_id].push_front(ArrivePlaceTime(target_location_id, target_time /*, onwards_leg_type = 'already_there') */));
        
        // Other variables
        this->final_destination_id = target_location_id;
        
        // Create the heap, for use as priority queue
        int max_values = this->locations.size();
        queue_values.resize(max_values + 1); // queue values is array with index location -> time of day (in minutes since midnight)
        boost::relaxed_heap<unsigned, LessValues> heap(max_values);

        // Put in initial value
        queue_values[target_location_id] = target_time; 
        heap.update(target_location_id);

        while(!heap.empty()) {
            // Find the item at top of queue
            LocationID nearest_location_id = heap.top();
            Minutes nearest_time= *queue_values[nearest_location_id];
            heap.pop();

            // If it is earlier than earliest departure we are going back to, then finish
            // if earliest_departure and nearest_datetime < earliest_departure:
            //    break

            // That item is now settled
            settled[nearest_location_id] = nearest_time;
            // ... copy the route into settled_routes, so we only return routes
            // we know we finished (rather than the partial, best-so-far that is
            // in routes)
            settled_routes[nearest_location_id] = routes[nearest_location_id];
            log(boost::format("settled location %s time %d") % this->locations[nearest_location_id].text_id % nearest_time);
            
            // Add all of its neighbours to the queue
            Adjacents adjacents;
            this->adjacent_location_times(adjacents, nearest_location_id, nearest_time);

            BOOST_FOREACH(AdjacentsPair p, adjacents) {
                LocationID location_id = p.first;
                ArrivePlaceTime arrive_place_time = p.second;
                if (queue_values[location_id]) {
                    // already in heap
                    Minutes current_priority = *queue_values[location_id];
                    if (arrive_place_time.when > current_priority) {
                        log(boost::format("updated location %s from priority %d to priority %d") % this->locations[location_id].text_id % current_priority % arrive_place_time.when);
                        queue_values[location_id] = arrive_place_time.when;
                        heap.update(location_id);
                        routes[location_id] = routes[nearest_location_id];
                        routes[location_id].push_front(arrive_place_time);
                    }
                } else {
                    // new priority to heap
                    log(boost::format("added location %s with priority %d") % this->locations[location_id].text_id % arrive_place_time.when);
                    queue_values[location_id] = arrive_place_time.when;
                    heap.push(location_id);
                    routes[location_id] = routes[nearest_location_id];
                    routes[location_id].push_front(arrive_place_time);
                }
            }
        }
    
        // return values are settled and settled_routes in parameters
    }

}; /*
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

int main(int argc, char * argv[]) {
    if (argc < 3) {
        printf("makeplan.cpp: fast index file prefix as first argument, output prefix as second argument, target arrival time in mins after midnight as second, target location at third");
        return 1;
    }

    std::string fastindexprefix = argv[1];
    std::string outputprefix = argv[2];
    Minutes target_minutes_after_midnight = atoi(argv[3]);
    std::string target_location_text_id = argv[4]; // e.g. "9100BHAMSNH";

    // Load timetables
    clock_t before_timetables = clock();
    PlanningATCO atco;
    atco.load_binary_timetable(fastindexprefix);
    clock_t after_timetables = clock();
    printf("loading timetables took: %f secs\n", double(after_timetables - before_timetables) / double(CLOCKS_PER_SEC));

    // Do route finding
    clock_t before_route = clock();
    Settled settled;
    Routes routes;
    LocationID target_location_id = atco.locations_by_text_id[target_location_text_id]; // 9100BHAMSNH
    atco.do_dijkstra(settled, routes, target_location_id, target_minutes_after_midnight);
    clock_t after_route = clock();
    printf("route finding took: %f secs\n", double(after_route - before_route) / double(CLOCKS_PER_SEC));

    // Output for grid
    std::string grid_time_file = outputprefix + ".txt";
    std::ofstream f;
    f.open(grid_time_file.c_str());
    BOOST_FOREACH(SettledPair p, settled) {
        LocationID l_id = p.first;
        Minutes min = target_minutes_after_midnight - p.second;
        int secs = min * 60;
        Location *l = &atco.locations[l_id];
        f << l->easting << " " << l->northing << " " << secs << "\n";
    }
    f.close();

    // Output for human
    std::string human_file = outputprefix + ".human.txt";
    std::ofstream g;
    g.open(human_file.c_str());
    g << "Journey times to " << target_location_text_id << " by " << target_minutes_after_midnight / 60 << ":" << target_minutes_after_midnight % 60 << "\n";
    BOOST_FOREACH(SettledPair p, settled) {
        LocationID l_id = p.first;
        Minutes when = target_minutes_after_midnight - p.second;
        Location *l = &atco.locations[l_id];
        g << l->text_id << " " << when << " mins\n";
        
        BOOST_FOREACH(ArrivePlaceTime arrive_place_time, routes[l_id]) {
            
            int hours = arrive_place_time.when / 60;
            int mins = arrive_place_time.when % 60;
            Location *rl = &atco.locations[arrive_place_time.location_id];
            g << "\tleave " << rl->text_id << " at " << hours << ":" << mins << std::endl;
        }
    }
    g.close();

    return 0;
};


