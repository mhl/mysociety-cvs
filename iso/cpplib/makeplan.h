//
// makeplan.h:
// Make timings for maps of journey times from NPTDR public transport route
// data. Reads input files made by iso/pylib/makefast.py.
//
// Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
// Email: francis@mysociety.org; WWW: http://www.mysociety.org/
//
// $Id: makeplan.h,v 1.2 2009-03-26 09:40:45 francis Exp $
//

// XXX all code is inline in this header file because a) I've got too
// used to scripting languages and b) we shouldn't be making a huge C++
// program where anyone minds anyway.

#include <set>
#include <map>
#include <vector>
#include <list>
#include <cstdio>
#include <fstream>

#include <sys/time.h>
#include <sys/resource.h>

#include <boost/foreach.hpp>
#include <boost/pending/relaxed_heap.hpp>

#include <stdarg.h>
#include <time.h>
#include <math.h>

typedef short Minutes; // after midnight (only needs to be a short, and we assume it is that for binary output)
#ifdef OUTPUT_ROUTE_DETAILS
std::string format_time(const Minutes& mins_after_midnight) {
    int hours = mins_after_midnight / 60;
    int mins = mins_after_midnight % 60;
    return (boost::format("%02d:%02d:00") % hours % mins).str();
}
#endif

typedef int LocationID;
class Location {
    public:
    std::string text_id; // e.g. 9100BANGOR
    int easting; // OS grid coordinate
    int northing; // OS grid coordinate

#ifdef DEBUG
    std::string toString() const {
        return (boost::format("Location(%s E:%d N:%d)") % this->text_id % this->easting % this->northing).str();
    }
#endif
};

class Hop {
    public:
    LocationID location_id;
    Minutes mins_arr; // minutes after midnight of arrival, or -1 if not set down stop
    Minutes mins_dep; // minutes after midnight of departure, or -1 if not pick up stop

#ifdef DEBUG
    std::string toString() const {
        return (boost::format("Hop(loc:%s arr:%d dep:%d)") % this->location_id % this->mins_arr % this->mins_dep).str();
    }
#endif

    bool is_pick_up() const {
        return mins_dep != -1;
    }
    bool is_set_down() const {
        return mins_arr != -1;
    }
};

typedef int JourneyID;
class Journey {
    public:
    std::string text_id; // e.g. CH-E7AB
    std::vector<Hop> hops;
    char vehicle_type; // T = train, B = bus

    const char* pretty_vehicle_type() const {
        if (vehicle_type == 'T') {
            return "train";
        } else if (vehicle_type == 'B') {
            return "bus";
        } else {
            assert(0);
        }
    }

#ifdef DEBUG
    std::string toString() const {
        return (boost::format("Journey(%s)") % this->text_id).str();
    }
#endif
};

class ArrivePlaceTime {
    /* Stores a location and date/time of arrival (including interchange wait)
    at that location. */

    public:

    LocationID location_id;
    Minutes when; // minutes after midnight

#ifdef OUTPUT_ROUTE_DETAILS
    char onwards_leg_type; // W = walk or J = journey or A = already there
    JourneyID onwards_journey_id;
    Minutes onwards_walk_time;
#endif

    ArrivePlaceTime(LocationID l_location_id, Minutes l_when
#ifdef OUTPUT_ROUTE_DETAILS
        , char l_onwards_leg_type, JourneyID l_onwards_journey_id, Minutes l_onwards_walk_time
#endif
    ) {
        this->location_id = l_location_id;
        this->when = l_when;

#ifdef OUTPUT_ROUTE_DETAILS
        this->onwards_leg_type = l_onwards_leg_type;
        this->onwards_journey_id = l_onwards_journey_id;
        this->onwards_walk_time = l_onwards_walk_time;
#endif
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
typedef std::pair<LocationID, Minutes> SettledPair;
typedef std::vector<SettledPair> Settled;
#ifdef OUTPUT_ROUTE_DETAILS
typedef std::list<ArrivePlaceTime> Route;
typedef std::map<LocationID, Route> Routes;
typedef std::pair<LocationID, std::list<ArrivePlaceTime> > RoutesPair;
#endif

// Stuff for relaxed_heap for Dijkstra's algorithm
// XXX must be global, is there a way to use relaxed_heap and this not be?
// Otherwise this whole thing can't be called from two threads using same data,
// which is a pain.
typedef std::vector<boost::optional<Minutes> > QueueValuesType;
QueueValuesType queue_values;
Location *queue_first_location = NULL;
struct LessValues
{
    bool operator()(unsigned x, unsigned y) const
    {
        debug_assert(queue_values[x] && queue_values[y]);
        if (queue_values[x] == queue_values[y]) {
            // This makes things the same distance in minutes come out of queue
            // in alphabetical order. That creates stability for comparing
            // output files.
            Location *l_x = &queue_first_location[x];
            Location *l_y = &queue_first_location[y];
            return l_x->text_id < l_y->text_id;
        }
        // reverse order - nearer to end time is better
        return queue_values[x] > queue_values[y];
    }
};

/* Loads and represents a set of ATCO-CIF files, and can generate large
sets of quickest routes from them.
*/
class PlanningATCO {
    public: 

    // input parameters
    int train_interchange_default;
    int bus_interchange_default;
    int number_of_locations;
    int number_of_journeys;

    float walk_speed; // metres /s ec
    float walk_time; // secs

    // input data structures
    std::vector<Location> locations;
    std::vector<Journey> journeys;

    // indices of various sorts
    std::map<std::string, LocationID> locations_by_text_id;

    typedef std::map<LocationID, std::set<JourneyID> > JourneysVisitingLocation;
    JourneysVisitingLocation journeys_visiting_location;

    typedef std::map<LocationID, double> NearbyLocationsInner;
    typedef std::vector<NearbyLocationsInner> NearbyLocations;
    typedef std::pair<LocationID, double> NearbyLocationsInnerPair;
    NearbyLocations nearby_locations;

    // working parameters
    LocationID final_destination_id;
    Minutes final_destination_time;
    // working outputs ... for dijkstra_output_store
    Settled settled;
#ifdef OUTPUT_ROUTE_DETAILS
    Routes routes;
#endif
    // ... for dijkstra_output_store_by_id
    std::vector<short> time_taken_by_location_id; // in delta minutes

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
        my_fread(&len, 1, sizeof(short), fp);
        // log(boost::format("_read_pascal_string len: %d") % len);
        std::string ret;
        ret.resize(len);
        my_fread(&ret[0], 1, len, fp);
        return ret;
    }

    /* Read in binary timetable files, exported by makefast.py */
    void load_binary_timetable(const std::string& l_in_prefix) {
        // Load in locations
        std::string location_filename = l_in_prefix + ".locations";
        FILE *fp = fopen(location_filename.c_str(), "rb");
        if (!fp) {
            fprintf(stderr, "Failed to open index file: %s\n", location_filename.c_str());
            exit(1);
        }
        my_fread(&this->number_of_locations, 1, sizeof(int), fp);
        log(boost::format("number of locations: %d") % this->number_of_locations);

        locations.resize(this->number_of_locations + 1);
        for (int i = 1; i <= this->number_of_locations; ++i) {
            LocationID id;
            my_fread(&id, 1, sizeof(LocationID), fp);
            assert(int(id) == i);

            Location *l = &this->locations[i];
            l->text_id = this->_read_pascal_string(fp);

            my_fread(&l->easting, 1, sizeof(l->easting), fp);
            my_fread(&l->northing, 1, sizeof(l->northing), fp);

            locations_by_text_id[l->text_id] = id;

            log(boost::format("loaded location: %s") % l->toString().c_str());
        }

        fclose(fp);

        // Load in journeys
        std::string journey_filename = l_in_prefix + ".journeys";
        fp = fopen(journey_filename.c_str(), "rb");
        if (!fp) {
            fprintf(stderr, "Failed to open index file: %s\n", journey_filename.c_str());
            exit(1);
        }
        my_fread(&this->number_of_journeys, 1, sizeof(int), fp);
        log(boost::format("number of journeys: %d") % this->number_of_journeys);

        journeys.resize(this->number_of_journeys + 1);
        for (int i = 1; i <= this->number_of_journeys; ++i) {
            JourneyID id;
            my_fread(&id, 1, sizeof(JourneyID), fp);
            assert(int(id) == i);

            Journey *j = &this->journeys[i];
            j->text_id = this->_read_pascal_string(fp);

            my_fread(&j->vehicle_type, 1, sizeof(char), fp);

            short number_of_hops;
            my_fread(&number_of_hops, 1, sizeof(number_of_hops), fp);
            log(boost::format("loaded journey: %s hops:%d") % j->toString().c_str() % number_of_hops);

            j->hops.resize(number_of_hops);
            for (int ii = 0; ii < number_of_hops; ++ii) {
                Hop hop;
                my_fread(&hop.location_id, 1, sizeof(hop.location_id), fp);
                short mins_arr, mins_dep; // file format uses shorts, whereas data structure is ints now
                my_fread(&mins_arr, 1, sizeof(mins_arr), fp);
                my_fread(&mins_dep, 1, sizeof(mins_dep), fp);
                hop.mins_arr = mins_arr;
                hop.mins_dep = mins_dep;
                j->hops[ii] = hop;
                log(boost::format("loaded hop: %s") % hop.toString().c_str());

                // update index
                journeys_visiting_location[hop.location_id].insert(id);
            }
        }
    }

    // Find out which stations are near to which others - naive agorithm.
    // This is never called, is just left here in case there are bugs in 
    // generate_proximity_index_fast, so the two can be compared.
    void generate_proximity_index_slow() {
        // Proximity index
        double nearby_max_distance = double(this->walk_speed) * double(this->walk_time);
        double nearby_max_distance_sq = nearby_max_distance * nearby_max_distance;

        this->nearby_locations.clear();
        this->nearby_locations.resize(this->number_of_locations + 1);
        for (LocationID location_id = 1; location_id <= this->number_of_locations; location_id++) {
            const Location &location = this->locations[location_id];
            double easting = location.easting;
            double northing = location.northing;
            for (LocationID other_location_id = location_id + 1; other_location_id <= this->number_of_locations; other_location_id++) {
                const Location &other_location = this->locations[other_location_id];
                double other_easting = other_location.easting;
                double other_northing = other_location.northing;
                double sqdist = (easting - other_easting)*(easting - other_easting)
                              + (northing - other_northing)*(northing - other_northing);

                if (sqdist < nearby_max_distance_sq) {
                    double dist = sqrt(sqdist);
                    log(boost::format("generate_proximity_index_slow: %s (%d,%d) is %f (sq %f, max %f) away from %s (%d,%d)") % location.text_id % easting % northing % dist % sqdist % nearby_max_distance % other_location.text_id % other_easting % other_northing);
                    nearby_locations[location_id][other_location_id] = dist;
                    nearby_locations[other_location_id][location_id] = dist;
                }
            }
        }
    }

    // Find out which stations are near to which others - with some spacial
    // partitioning to speed it up
    void generate_proximity_index_fast() {
        double nearby_max_distance = double(this->walk_speed) * double(this->walk_time);
        double nearby_max_distance_sq = nearby_max_distance * nearby_max_distance;

        // we put a grid of boxes over the plane
        int boxsize = 1000;
        int boxscanrange = int(nearby_max_distance / double(boxsize)) + 1;

        // store the loctions in each box cell, for later speed
        typedef std::map<int, std::set<LocationID> > SpaceFindInner;
        typedef std::map<int, SpaceFindInner > SpaceFind;
        SpaceFind sf;
        for (LocationID location_id = 1; location_id <= this->number_of_locations; location_id++) {
            const Location &location = this->locations[location_id];
            double easting = location.easting;
            double northing = location.northing;

            int box_e = int(easting) / boxsize;
            int box_n = int(northing) / boxsize;

            sf[box_e][box_n].insert(location_id);
        }

        // do actual calculation
        this->nearby_locations.clear();
        this->nearby_locations.resize(this->number_of_locations + 1);
        for (LocationID location_id = 1; location_id <= this->number_of_locations; location_id++) {
            const Location &location = this->locations[location_id];
            double easting = location.easting;
            double northing = location.northing;

            // loop over boxes that we have to cover in order to definitely reach everything in range 
            int box_e_center = int(easting) / boxsize;
            int box_n_center = int(northing) / boxsize;
            for (int box_e = box_e_center - boxscanrange; box_e <= box_e_center + boxscanrange; ++box_e) {
                for (int box_n = box_n_center - boxscanrange; box_n <= box_n_center + boxscanrange; ++box_n) {
                    SpaceFind::iterator it = sf.find(box_e);
                    if (it == sf.end()) {
                        continue;
                    }
                    SpaceFindInner& sfi = it->second;
                    SpaceFindInner::iterator it2 = sfi.find(box_n);
                    if (it2 == sfi.end()) {
                        continue;
                    }

                    // see which of the locations we have to check *are* actually near enough
                    const std::set<LocationID>& other_location_list = it2->second;
                    BOOST_FOREACH(const LocationID& other_location_id, other_location_list) {
                        // ignore own location
                        if (location_id == other_location_id) {
                            continue;
                        }
                        const Location &other_location = this->locations[other_location_id];

                        // more precise accuracy check
                        double other_easting = other_location.easting;
                        double other_northing = other_location.northing;
                        double sqdist = (easting - other_easting)*(easting - other_easting)
                                      + (northing - other_northing)*(northing - other_northing);

                        if (sqdist < nearby_max_distance_sq) {
                            double dist = sqrt(sqdist);
                            log(boost::format("generate_proximity_index_fast: %s (%d,%d) is %f (sq %f, max %f) away from %s (%d,%d)") % location.text_id % easting % northing % dist % sqdist % nearby_max_distance % other_location.text_id % other_easting % other_northing);
                            nearby_locations[location_id][other_location_id] = dist;
                        }
                    }

                }
            }

        }

    }
    
    // Given a grid coordinate, find the nearest station.
    LocationID find_nearest_station_to_point(double easting, double northing) {
        double best_dist_so_far_sq = -1;
        LocationID best_location_id = -1;
        for (LocationID location_id = 1; location_id <= this->number_of_locations; location_id++) {
            const Location &location = this->locations[location_id];
            double dist_sq = (easting - location.easting)*(easting - location.easting)
                          + (northing - location.northing)*(northing - location.northing);

            if (dist_sq < best_dist_so_far_sq || best_dist_so_far_sq < 0) {
                log(boost::format("find_nearest_station_to_point: %s (%d,%d) is sqdist %f away from grid %d,%d") % location.text_id % easting % northing % dist_sq % easting % northing);
                best_dist_so_far_sq = dist_sq;
                best_location_id = location_id;
            }
        }
        assert(best_location_id != -1);
        return best_location_id;
    }

#ifdef DEBUG
    /* Use this for testing the two proximity index functions above */
    void dump_nearby_locations() {
        log("---------------------------------------\n");
        for (LocationID location_id = 1; location_id <= this->number_of_locations; location_id++) {
            Location &location = this->locations[location_id];
            const NearbyLocationsInner& nearby_locations_inner = this->nearby_locations[location_id];
            BOOST_FOREACH(const NearbyLocationsInnerPair& p, nearby_locations_inner) {
                const LocationID& other_location_id = p.first;
                Location &other_location = this->locations[other_location_id];
                double dist = p.second;

                log(boost::format("dump_nearby_locations: %s (%d,%d) is %d away from %s (%d,%d)") % location.text_id % location.easting % location.northing % dist % other_location.text_id % other_location.easting % other_location.northing)
            }
        }
        log("---------------------------------------\n");
    }
#endif

    /* Adjacency function for use with Dijkstra's algorithm on earliest
    time to arrive somewhere.  Given a location and a date/time, it finds every
    other station from which you can get there on time by one *direct*
    train/bus. 

    Adjacents is map from location to time at that location, and
    is the data structure we are going to return from this function.
    */
    void adjacent_location_times(Adjacents &adjacents, LocationID target_location_id, Minutes target_arrival_time) {
        // Check that there are journeys visiting this location
        log(boost::format("adjacent_location_times target_location: %s target_arrival_time: %s") % this->locations[target_location_id].text_id % format_time(target_arrival_time));
        JourneysVisitingLocation::iterator it = this->journeys_visiting_location.find(target_location_id);
        if (it == journeys_visiting_location.end()) {
            // This can happen, for example, with locations that are only
            // stopped at at the weekend, when it is a weekday. The fastplan.py
            // code doesn't strip such cases.
        } else {
            // Go through every journey visiting the location
            const std::set<JourneyID>& journey_list = it->second;
            BOOST_FOREACH(const JourneyID& journey_id, journey_list) {
                log(boost::format("\tconsidering journey: %s") % this->journeys[journey_id].text_id)
                this->_adjacent_location_times_for_journey(target_location_id, target_arrival_time, adjacents, journey_id);
            }
        }

        // Add nearby locations
        this->_nearby_locations(target_location_id, target_arrival_time, adjacents);
    }

    /* Private helper function. Store a time we can leave a station, if it
    is later than previous direct routes we have for leaving from that
    station and arriving at target. */
    void _add_to_adjacents(ArrivePlaceTime &arrive_place_time, Adjacents &adjacents) {
        // This is written to minimise the number of searches of the map, as it
        // is performance critical. So, uses "insert" rather than "[]".
        AdjacentsPair ap(arrive_place_time.location_id, arrive_place_time);
        std::pair<Adjacents::iterator, bool> p = adjacents.insert(ap);
        if (!p.second) {
            // Element already exists, update it in place if new one is better
            const Adjacents::iterator& it = p.first;
            if (arrive_place_time.when > it->second.when) {
                it->second = arrive_place_time;
            }
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
        #ifdef DEBUG
        Location *target_location = &this->locations[target_location_id];
        int target_easting = this->locations[target_location_id].easting;
        int target_northing = this->locations[target_location_id].northing;
        #endif

        const NearbyLocationsInner &nearby_locations_inner = this->nearby_locations[target_location_id];
        BOOST_FOREACH(const NearbyLocationsInnerPair& p, nearby_locations_inner) {
            const LocationID& location_id = p.first;
            double dist = p.second;

            #ifdef DEBUG
            Location *location = &this->locations[location_id];
            log(boost::format("_nearby_locations: %s (%d,%d) is %d away from %s (%d,%d)") % location->text_id % location->easting % location->northing % dist % target_location->text_id % target_easting % target_northing)
            #endif

            Minutes walk_time = this->_walk_time_apart(dist);
            Minutes walk_departure_time = target_arrival_time - walk_time;
            ArrivePlaceTime arrive_time_place(location_id, walk_departure_time
#ifdef OUTPUT_ROUTE_DETAILS
                , 'W', -1, walk_time
#endif
            );
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
        const Journey& journey = this->journeys[journey_id];

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
        BOOST_FOREACH(const Hop& hop, journey.hops) {
            // Find hops that arrive at the target
            if (hop.location_id != target_location_id) {
                continue;
            }
            if (!hop.is_set_down()) {
                continue;
            }
            Minutes possible_arrival_time_at_target_location = hop.mins_arr;
            log(boost::format("\t\tarrival time %s at target location %s") % format_time(possible_arrival_time_at_target_location) % this->locations[target_location_id].text_id);
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
            log(boost::format("\t\twhich are all too late for %s by %s with interchange time %d so not using journey") % this->locations[target_location_id].text_id % format_time(target_arrival_time) % interchange_time);
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
        BOOST_FOREACH(const Hop& hop, journey.hops) {
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
            ArrivePlaceTime arrive_place_time(hop.location_id, departure_time
#ifdef OUTPUT_ROUTE_DETAILS
                , 'J', journey_id, -1
#endif
            );
#ifdef DEBUG
            log(boost::format("\t\t\tadding stop: %s %s") % this->locations[hop.location_id].text_id % format_time(departure_time));
#endif
            this->_add_to_adjacents(arrive_place_time, adjacents);
        }
    }

    /* Method pointer type for what to do with results from do_dijkstra.
     * Various dijkstra_output_* methods below are suitable. */
    typedef void (PlanningATCO::*ResultFunctionPointer)(const LocationID&, const Minutes&
#ifdef OUTPUT_ROUTE_DETAILS
        , const Route&
#endif
    );

    /*
    Run Dijkstra's algorithm to find latest departure time from all locations to
    arrive at the target location by the given time.

    result_function_pointer - which of various dijkstra_output_* functions to use for output
    target_location_id - station id to go to, e.g. 9100AYLSBRY or 210021422650
    target_time - when we want to arrive by, minutes after midnight
    earliest_departure - what minute in day to stop when we get back to
    */
    void do_dijkstra(ResultFunctionPointer result_function_pointer,
        const LocationID target_location_id, const Minutes target_time, const Minutes earliest_departure
    ) {
#ifdef OUTPUT_ROUTE_DETAILS
        Routes routes; // how to get there
        routes[target_location_id].push_front(ArrivePlaceTime(target_location_id, target_time, 'A', -1, -1));
#endif

        // Initialize data structures for output if appropriate
        if (result_function_pointer == &PlanningATCO::dijkstra_output_store_by_id) {
            time_taken_by_location_id.resize(this->number_of_locations + 1);
            std::fill(time_taken_by_location_id.begin(), time_taken_by_location_id.end(), -1);
        } else if (result_function_pointer == &PlanningATCO::dijkstra_output_store) {
            this->settled.clear();
#ifdef OUTPUT_ROUTE_DETAILS
            this->routes.clear();
#endif
        }
        
        // Other variables
        this->final_destination_id = target_location_id;
        this->final_destination_time = target_time;
        
        // Create the heap, for use as priority queue
        int max_values = this->locations.size();
        queue_values.resize(max_values + 1); // queue values is array with index location -> time of day (in minutes since midnight)
        queue_first_location = &this->locations[0];
        typedef std::pair<unsigned, LessValues> HeapPair;
        boost::relaxed_heap<unsigned, LessValues> heap(max_values);
        std::set<LocationID> settled_set;

        // Put in initial value
        queue_values[target_location_id] = target_time; 
        heap.update(target_location_id);

        while(!heap.empty()) {
            // Find the item at top of queue
            LocationID nearest_location_id = heap.top();
            Minutes nearest_time= *queue_values[nearest_location_id];
            heap.pop();
            queue_values[nearest_location_id] = boost::optional<Minutes>();

            // If it is earlier than earliest departure we are going back to, then finish
            if (nearest_time < earliest_departure) {
                break;
            }

            // That item is now settled
            settled_set.insert(nearest_location_id);
            // ... do whatever is required with it
            (*this.*result_function_pointer)(nearest_location_id, nearest_time
#ifdef OUTPUT_ROUTE_DETAILS
                , routes[nearest_location_id]
#endif
            );
            log(boost::format("settled location %s time %s") % this->locations[nearest_location_id].text_id % format_time(nearest_time));
            
            // Add all of its neighbours to the queue
            Adjacents adjacents;
            this->adjacent_location_times(adjacents, nearest_location_id, nearest_time);

            BOOST_FOREACH(const AdjacentsPair& p, adjacents) {
                const LocationID& location_id = p.first;
                #ifdef DEBUG
                const Location& location = this->locations[location_id];
                #endif 
                const ArrivePlaceTime& arrive_place_time = p.second;
                log(boost::format("considering direct connecting station: %s priority %s") % location.text_id.c_str() % format_time(arrive_place_time.when));
                if (queue_values[location_id]) {
                    // already in heap
                    Minutes current_priority = *queue_values[location_id];
                    debug_assert(settled_set.find(location_id) == settled_set.end());
                    if (arrive_place_time.when > current_priority) {
                        log(boost::format("\tupdated location %s from priority %s to priority %s") % this->locations[location_id].text_id % format_time(current_priority) % format_time(arrive_place_time.when));
                        queue_values[location_id] = arrive_place_time.when;
                        heap.update(location_id);
#ifdef OUTPUT_ROUTE_DETAILS
                        routes[location_id] = routes[nearest_location_id];
                        routes[location_id].push_front(arrive_place_time);
#endif
                    } else {
                        log(boost::format("\tlocation %s already in heap priority %s") % this->locations[location_id].text_id % format_time(current_priority));
                    }
                } else {
                    if (settled_set.find(location_id) == settled_set.end()) {
                        // new priority to heap
                        log(boost::format("\tadded location %s with priority %s") % this->locations[location_id].text_id % format_time(arrive_place_time.when));
                        queue_values[location_id] = arrive_place_time.when;
                        heap.push(location_id);
#ifdef OUTPUT_ROUTE_DETAILS
                        routes[location_id] = routes[nearest_location_id];
                        routes[location_id].push_front(arrive_place_time);
#endif
                    } else {
                        log(boost::format("\tlocation %s already settled") %  this->locations[location_id].text_id);
                    }
                }
            }
        }
    
        // return values are sent via the result_function_pointer parameter
    }

    // For do_dijkstra output. Store in order of the journey, and if compiled
    // to also store the route. pretty_print_routes below can print output from
    // this. Output arrays are cleared in do_dijkstra if this is passed in.
    void dijkstra_output_store(const LocationID& location_id, const Minutes& when
#ifdef OUTPUT_ROUTE_DETAILS
        , const Route& route
#endif
    ) {
        this->settled.push_back(std::make_pair(location_id, when));
#ifdef OUTPUT_ROUTE_DETAILS
        this->routes[location_id] = route;
#endif
    }

    // For do_dijkstra output. Store in array, so can find time for a
    // particular location quickly. Array is cleared in do_dijkstra is this is
    // passed in.
    void dijkstra_output_store_by_id(const LocationID& location_id, const Minutes& when) {
        const Minutes& mins = this->final_destination_time - when;
        time_taken_by_location_id[location_id] = mins;
    }

    // For do_dijkstra output. Output results as they come to stdout. Don't store anything.
    void dijkstra_output_stream_stdout(const LocationID& location_id, const Minutes& when
#ifdef OUTPUT_ROUTE_DETAILS
        , const Route& route
#endif
    ) {
        const Minutes& mins = this->final_destination_time - when;
        int secs = mins * 60;
        Location *l = &this->locations[location_id];
        printf("%d %d %d\n", l->easting, l->northing, secs);
    }

#ifdef OUTPUT_ROUTE_DETAILS
    /* do_dijkstra returns a journey routes array, this prints it in a human readable format. */
    std::string pretty_print_routes(const Settled& settled, const Routes& routes) {
        const Location& final_destination = this->locations[this->final_destination_id];
        std::string ret = (boost::format("Journey times to %s by %s\n") % final_destination.text_id % format_time(this->final_destination_time)).str();
        BOOST_FOREACH(const SettledPair& p, settled) {
            const LocationID& l_id = p.first;
            const Location& from_location = this->locations[l_id];
            int mins = this->final_destination_time - p.second;
            const Route& route = routes.find(l_id)->second;

            ret += (boost::format("From %s in %d mins:\n") % from_location.text_id % mins).str();

            for (Route::const_iterator it = route.begin(); it != route.end(); it++) {
                const ArrivePlaceTime& stop = *it;
                const Location& location = this->locations[stop.location_id];
                if (stop.onwards_leg_type == 'A') {
                    ret += (boost::format("    You've arrived at %s\n") % location.text_id).str();
                    continue;
                }
                it++; const ArrivePlaceTime& next_stop = *it; it--;
                const Location& next_location = this->locations[next_stop.location_id];
                
                if (stop.onwards_leg_type == 'W') {
                    ret += (boost::format("    Leave by walking to %s, will take %d mins\n") % next_location.text_id % stop.onwards_walk_time).str();
                } else if (stop.onwards_leg_type == 'J') {
                    const Journey& journey = this->journeys[stop.onwards_journey_id];
                    ret += (boost::format("    Leave %s by %s on %s at ") % location.text_id.c_str() % journey.pretty_vehicle_type() % journey.text_id.c_str()).str();
                    BOOST_FOREACH(const Hop& hop, journey.hops) {
                        if (hop.is_pick_up() && hop.location_id == stop.location_id) {
                            ret += (format_time(hop.mins_dep).c_str());
                        }
                    }

                    ret += (boost::format(", arriving %s at ") % next_location.text_id).str();
                    BOOST_FOREACH(const Hop& hop, journey.hops) {
                        if (hop.is_set_down() && hop.location_id == next_stop.location_id) {
                            ret += (format_time(hop.mins_arr).c_str());
                        }
                    }

                    ret += ("\n");
                } else {
                    assert(0);
                }
            }
        }
        return ret;
    }
#endif

}; 


