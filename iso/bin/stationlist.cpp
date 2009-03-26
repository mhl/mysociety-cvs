//
// stationlist.cpp:
// Given a fastplan index, outputs list of stations, their coordinates, and the
// number of journeys that pass through them (for culling).
//
// Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
// Email: francis@mysociety.org; WWW: http://www.mysociety.org/
//
// $Id: stationlist.cpp,v 1.2 2009-03-26 09:40:45 francis Exp $
//

#include <math.h> // something weird in /usr/include/bits/mathcalls.h means this must be included from top level file

#include "../../cpplib/mysociety_error.h"
#include "../cpplib/makeplan.h"

#include <iostream>

int main(int argc, char * argv[]) {
    if (argc != 2) {
        fprintf(stderr, "stationlist.cpp:\n  fast index file prefix as only argument\n(%d args counted)\n", argc);
        return 1;
    }
    std::string fastindexprefix = argv[1];

    PlanningATCO atco;
    atco.load_binary_timetable(fastindexprefix);
    
    for (LocationID location_id = 1; location_id <= atco.number_of_locations; location_id++) {
        Location *l = &atco.locations[location_id];
        int journey_count = atco.journeys_visiting_location[location_id].size();
        std::cout << l->text_id << " " << l->easting << " " << l->northing << " " << journey_count << "\n";
    }

    return 0;
};


