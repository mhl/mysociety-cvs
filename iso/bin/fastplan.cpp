//
// fastplan.cpp:
// Command line program to generate lat/lon/time file file for a particular
// destination. See cpplib/makeplan.h for bulk of code.
//
// Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
// Email: francis@mysociety.org; WWW: http://www.mysociety.org/
//
// $Id: fastplan.cpp,v 1.8 2009-04-24 14:16:44 francis Exp $
//

// Usage:
// g++ -g fastplan.cpp -DDEBUG
// ./a.out /home/francis/toobig/nptdr/gen/nptdr-B32QD-40000 540 9100BHAMSNH
//

#include <math.h> // something weird in /usr/include/bits/mathcalls.h means this must be included from top level file

#include "../../cpplib/mysociety_error.h"
#include "../cpplib/makeplan.h"
#include "../cpplib/performance_monitor.h"

int main(int argc, char * argv[]) {
    if (argc < 7) {
        fprintf(stderr, "fastplan.cpp:\n  fast index file prefix as first argument\n  output prefix (or 'stream' for stdout incremental) as second\n  target arrival time in mins after midnight as third\n  target location as fourth\n  earliest departure in mins after midnight to go back to as fifth\n  easting, northing to use to find destination if destination is 'coordinate' as sixth and seventh\n");
        return 1;
    }

    std::string fastindexprefix = argv[1];
    std::string outputprefix = argv[2];
    Minutes target_minutes_after_midnight = atoi(argv[3]);
    std::string target_location_text_id = argv[4]; // e.g. "9100BHAMSNH";
    Minutes earliest_departure = atoi(argv[5]);
    double easting = atoi(argv[6]);
    double northing = atoi(argv[7]);

    // Load timetables
    PerformanceMonitor pm;
    PlanningATCO atco;
    atco.load_binary_timetable(fastindexprefix);
    pm.display("loading timetables took");
    atco.generate_proximity_index_fast();
    pm.display("generating proximity index took");

    // Find nearest place from grid reference
    LocationID target_location_id;
    if (target_location_text_id == "coordinate") {
        target_location_id = atco.find_nearest_station_to_point(easting, northing);
    } else {
        target_location_id = atco.locations_by_text_id[target_location_text_id]; // 9100BHAMSNH
    }
    Location *target_location = &atco.locations[target_location_id];
    fprintf(stderr, "target location: %s\n", target_location->text_id.c_str());

    // Work out what to do with output
    PlanningATCO::ResultFunctionPointer result_function_pointer;
    if (outputprefix == "stream") {
        result_function_pointer = &PlanningATCO::dijkstra_output_stream_stdout;
    } else {
        result_function_pointer = &PlanningATCO::dijkstra_output_store;
    }

    // Do route finding
    atco.do_dijkstra(
        result_function_pointer,
        target_location_id, target_minutes_after_midnight,
        earliest_departure
    );
    pm.display("route finding took");

    if (outputprefix != "stream") {
        // Output for grid
        std::string grid_time_file = outputprefix + ".txt";
        std::ofstream f;
        f.open(grid_time_file.c_str());
        for (LocationID l_id = 1; l_id <= atco.number_of_locations; ++l_id) {
            if (atco.settled[l_id] == MINUTES_NULL) {
                continue;
            }

            const Minutes& min = target_minutes_after_midnight - atco.settled[l_id];

            int secs = min * 60;
            Location *l = &atco.locations[l_id];
            f << l->easting << " " << l->northing << " " << secs << " " << "\n";
        }
        f.close();
        pm.display("grid output took");

#ifdef OUTPUT_ROUTE_DETAILS
        // Output for human
        std::string human_file = outputprefix + "-human.txt";
        std::ofstream g;
        g.open(human_file.c_str());
        g << atco.pretty_print_routes();
        g.close();
        pm.display("human output took");
#endif
    }

    return 0;
};


