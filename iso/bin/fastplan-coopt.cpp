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
// $Id: fastplan-coopt.cpp,v 1.10 2009-04-24 16:45:49 francis Exp $
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

    // Turn off buffering, so progress goes to parent isodaemon.py quickly
    setbuf(stderr, NULL);
    setbuf(stdout, NULL);

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
        pm.reset();

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
            std::string arg1, arg2, arg3, arg4, arg5;
            std::cin >> arg1 >> arg2 >> arg3 >> arg4 >> arg5;

            std::string output_binary = arg1.c_str();
            std::string output_routes = arg2.c_str();
            Minutes target_minutes_after_midnight = atoi(arg3.c_str());
            Minutes earliest_departure = atoi(arg4.c_str());
            std::string target_location_text_id = arg5;
    
            LocationID target_location_id = atco.locations_by_text_id[target_location_text_id];
            fprintf(stdout, "target location: %d %s\n", target_location_id, target_location_text_id.c_str());

            // Do route finding
            atco.do_dijkstra(
                &PlanningATCO::dijkstra_output_store_by_id,
                target_location_id, target_minutes_after_midnight,
                earliest_departure
            );
            pm.display("route finding took");

            // Output times
            FILE *fp = fopen(output_binary.c_str(), "wb");
            if (!fp) {
                fprintf(stdout, "failed to make output file: %s\n", output_binary.c_str());
                return 1;
            }
            my_fwrite(&atco.time_taken_by_location_id[0], atco.time_taken_by_location_id.size(), sizeof(Minutes), fp);
            fclose(fp);
#ifdef OUTPUT_ROUTE_DETAILS
            // Output routes
            FILE *fp2 = fopen(output_routes.c_str(), "wb");
            if (!fp2) {
                fprintf(stdout, "failed to make routes output file: %s\n", output_routes.c_str());
                return 1;
            }
            my_fwrite(&atco.routes[0], atco.routes.size(), sizeof(RouteNode), fp2);
            fclose(fp2);
#endif
            pm.display("binary output took");
        } else if (command == "fork") {
            // fork daemon - note this happens after timetable loading, so RAM of the timetable
            // data structures is shared between instances. Prameters are file descriptors
            // to use for stdin/stdout/stderr in the child after the fork. These must have
            // been set up by the parent process of the original daemon instance, so it can
            // talk to each child separately.
            std::string arg1, arg2, arg3;
            std::cin >> arg1 >> arg2 >> arg3;

            int newfd0, newfd1, newfd2;
            newfd0 = atoi(arg1.c_str());
            newfd1 = atoi(arg2.c_str());
            newfd2 = atoi(arg3.c_str());

            int pid = fork();
            if (pid == -1) {
                fprintf(stdout, "failed to fork: fds %d %d %d\n", newfd0, newfd1, newfd2); 
                return 1;
            }
            if (pid == 0) {
                // Child
                dup2(newfd0, 0);
                dup2(newfd1, 1);
                dup2(newfd2, 2);
                continue;
            }
            // Parent, continue
            fprintf(stdout, "done fork: child is using fds %d %d %d\n", newfd0, newfd1, newfd2); 
        } else if (command == "info") {
            fprintf(stdout, "fastplan-coopt: pid %d\n", getpid());
        } else {
            fprintf(stdout, "unknown command %s\n", command.c_str());
        }
    }

    return 0;
};


