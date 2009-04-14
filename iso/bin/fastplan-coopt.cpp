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
// $Id: fastplan-coopt.cpp,v 1.7 2009-04-14 16:13:37 francis Exp $
//

// Example one off runs (the EOF from stdin will make the program exit after one command)
//echo plan 540 0 450445 207017 | ./fastplan-coopt /home/francis/toobig/nptdr/gen/fastindex-713f1c5e34a0-2008-10-07 >out
//echo binplan /tmp/map1.iso 540 0 340002053CR | ./fastplan-coopt /home/francis/toobig/nptdr/gen/fastindex-713f1c5e34a0-2008-10-07

#include <math.h> // something weird in /usr/include/bits/mathcalls.h means this must be included from top level file

#include "../../cpplib/mysociety_error.h"
#include "../cpplib/makeplan.h"
#include "../cpplib/performance_monitor.h"

#include <iostream>

int main(int argc, char * argv[]) {
    if (argc != 2) {
        fprintf(stdout, "fastplan-coopt.cpp:\n  fast index file prefix as only argument\n(%d args counted)\n", argc);
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
            // reference as text.
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
        } else if (command == "binplan") {
            // Make a plan, and output binary file of coordinates to use.
            std::string arg1, arg2, arg3, arg4;
            std::cin >> arg1 >> arg2 >> arg3 >> arg4;

            std::string output_binary = arg1.c_str();
            Minutes target_minutes_after_midnight = atoi(arg2.c_str());
            Minutes earliest_departure = atoi(arg3.c_str());
            std::string target_location_text_id = arg4;
    
            LocationID target_location_id = atco.locations_by_text_id[target_location_text_id];
            fprintf(stdout, "target location: %d %s\n", target_location_id, target_location_text_id.c_str());

            // Do route finding
            atco.do_dijkstra(
                &PlanningATCO::dijkstra_output_store_by_id,
                target_location_id, target_minutes_after_midnight,
                earliest_departure
            );
            pm.display("route finding took");

            // Output
            FILE *fp = fopen(output_binary.c_str(), "wb");
            if (!fp) {
                fprintf(stdout, "failed to make output file: %s\n", output_binary.c_str());
                return 1;
            }
            my_fwrite(&atco.time_taken_by_location_id[0], atco.time_taken_by_location_id.size(), sizeof(Minutes), fp);
            fclose(fp);
            pm.display("binary output took");
        } else {
            fprintf(stdout, "unknown command %s\n", command.c_str());
        }
    }

    return 0;
};


