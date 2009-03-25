//
// fastplan-coopt.cpp:
// Version of fastplan.cpp for calling from Python daemon. Takes commands
// on stdin, outputs plans on stdout. Only loading the timetables once,
// can then sit and generate any number of plans. Exits when stdin 
// reaches eof.
//
// Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
// Email: francis@mysociety.org; WWW: http://www.mysociety.org/
//
// $Id: fastplan-coopt.cpp,v 1.2 2009-03-25 12:05:24 francis Exp $
//

#include <math.h> // something weird in /usr/include/bits/mathcalls.h means this must be included from top level file

#include "../../cpplib/mysociety_error.h"
#include "../cpplib/makeplan.h"
#include "../cpplib/performance_monitor.h"

#include <iostream>

int main(int argc, char * argv[]) {
    if (argc != 2) {
        fprintf(stderr, "fastplan-coopt.cpp:\n  fast index file prefix as only argument\n(%d args counted)\n", argc);
        return 1;
    }
    std::string fastindexprefix = argv[1];

    // Load timetables
    PerformanceMonitor pm(stdout); // output everything to stdout except errors, so easier for Python script
    PlanningATCO atco;
    atco.load_binary_timetable(fastindexprefix);
    atco.generate_proximity_index_fast();
    pm.display("loading took");
    
    // Read commands from stdin
    while (1) {
        std::string command;
        std::cin >> command;

        if (std::cin.eof()) {
            break;
        } else if (command == "plan") {
            // Make a plan, and output the time coordinates to get to each grid
            // reference.
            std::string arg1, arg2, arg3, arg4;
            std::cin >> arg1 >> arg2 >> arg3 >> arg4;

            Minutes target_minutes_after_midnight = atoi(arg1.c_str());
            Minutes earliest_departure = atoi(arg2.c_str());
            double easting = atoi(arg3.c_str());
            double northing = atoi(arg4.c_str());

            // Find nearest place from grid reference
            LocationID target_location_id;
            target_location_id = atco.find_nearest_station_to_point(easting, northing);
            Location *target_location = &atco.locations[target_location_id];
            fprintf(stdout, "target location: %s\n", target_location->text_id.c_str());

            // Do route finding
            atco.do_dijkstra(
                &PlanningATCO::dijkstra_output_stream_stdout,
                target_location_id, target_minutes_after_midnight,
                earliest_departure
            );
            pm.display("route finding took");
        } else {
            fprintf(stderr, "unknown command %s\n", command.c_str());
        }
    }

    return 0;
};


