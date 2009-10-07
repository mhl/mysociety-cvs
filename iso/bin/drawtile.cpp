//
// drawtile.cpp:
//
// Renders a contour tile. Input is a data set, which is a series of locations
// with values. e.g. House prices. And the X/Y/Zoom fo the web map tile to render.
// Output is s PNG of the file with colour-value contours on it.
//
// All coordinates everywhere are spherical mercator.
//
// Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
// Email: francis@mysociety.org; WWW: http://www.mysociety.org/
//
// $Id: drawtile.cpp,v 1.11 2009-10-07 08:35:31 francis Exp $
//

// TODO:
// Convert box set thing to use own radius (which is really then separate from the effect radius which varies per tile now)
// Nearby pixel radius check should surely be pixel_radius * 2 not just pixel_radius
// Move im to be member of Tile?
// remove effect_radius completely

#include <math.h> 
#include <gd.h>
#include <assert.h>
#include <float.h>

#include <sys/types.h>
#include <sys/stat.h>

#include <vector>
#include <list>
#include <map>
#include <algorithm>

#include "../../cpplib/mysociety_error.h"
#include "../../cpplib/mysociety_geo.h"
#include "../cpplib/performance_monitor.h"

/* Any size of tile you like, as long as it is 256x256 pixels */
#define IMAGE_WIDTH 256
#define IMAGE_HEIGHT 256
double image_diagonal = sqrt(IMAGE_WIDTH * IMAGE_WIDTH + IMAGE_HEIGHT * IMAGE_HEIGHT);
int zoom_levels = 20;
gdImagePtr im;

/* Limits for spherical mercator */
// bbox = "-20037508.34,-20037508.34,20037508.34,20037508.34"
double merc_x_orig_min = -20037508.34;
double merc_y_orig_min = -20037508.34;
double merc_x_orig_max = 20037508.34;
double merc_y_orig_max = 20037508.34;
double merc_max_resolution = 156543.0339;

int no_data_colour = -1;

/* Stats for debugging */
int plot_count = 0;
int sqrt_count = 0;

/////////////////////////////////////////////////////////////////////
// Plotting on tiles

/* Length of vector */
double calc_dist(double x, double y) {
    sqrt_count++;
    return sqrt(x * x + y * y);
}

/* Square of length of vector */
double calc_dist_sq(double x, double y) {
    return x * x + y * y;
}

/* Optimised version of length of vector. Only takes pixel lengths
 * which are shorter than the size of the tile as input, caches
 * results for output. */
double sqrt_cache[IMAGE_WIDTH+1][IMAGE_HEIGHT+1];
bool sqrt_cache_initialised = false;
void calc_dist_fast_int_initialise() {
    for (int x = 0; x <= IMAGE_WIDTH; x++) {
        for (int y = 0; y <= IMAGE_HEIGHT; y++) {
            sqrt_cache[x][y] = sqrt(double(x * x + y * y));
        }
    }

    sqrt_cache_initialised = true;
}
double calc_dist_fast_int_on_tile(int x, int y) {
    // debug_log(boost::format("calc_dist_fast_int_on_tile: %d %d") % x % y);
    
    x = abs(x); y = abs(y);
    assert(x >= 0 && y >= 0 && x <= IMAGE_WIDTH && y <= IMAGE_HEIGHT);
    assert(sqrt_cache_initialised);

    double result = sqrt_cache[x][y];
    return result;
}

/* Another optimised distance function. */
typedef std::map<int, double> SqrtCacheColumn;
typedef std::map<int, SqrtCacheColumn> SqrtCache;
SqrtCache sqrt_cache_flex;
double calc_dist_fast_int_anywhere(int x, int y) {
    SqrtCache::iterator it = sqrt_cache_flex.find(x);
    if (it != sqrt_cache_flex.end()) {
        SqrtCacheColumn::iterator it2 = it->second.find(y);
        if (it2 != it->second.end()) {
            return it2->second;
        }
    }

    sqrt_count++;
    double value = sqrt(double(x * x + y * y));
    sqrt_cache_flex[x][y] = value;
    return value;
}

/* Plot a pixel on a tile, check values in range.
   Note: GD has Y going down the page, in spherical mercator coords it goes up.
   That's why we flip the Y value just before drawing.
*/
void guarded_plot(int x, int y, int col) {
    plot_count++;
    if (x >= 0 && y >= 0 && x < IMAGE_WIDTH && y < IMAGE_HEIGHT) {
        //debug_log(boost::format("plotting: %d %d colour: %d") % x % y % col);
        gdImageTrueColorPixel(im, x, IMAGE_HEIGHT - 1 - y) = col; 
    }
}

/* Plot a pixel on a tile, check values in range, but use the minimum value */
void guarded_min_plot(int x, int y, int col) {
    plot_count++;
    if (x >= 0 && y >= 0 && x < IMAGE_WIDTH && y < IMAGE_HEIGHT) {
        int current_col = gdImageTrueColorPixel(im, x, IMAGE_HEIGHT - 1 - y);
        if (current_col == 0 || col < current_col) {
            gdImageTrueColorPixel(im, x, IMAGE_HEIGHT - 1 - y) = col;
        }
    }
}

/////////////////////////////////////////////////////////////////////
// Tiles - transforming between mercator position and tile URL/zoom

class Tile {
    public:
    Tile(int l_zoom, int l_google_url_x, int l_google_url_y) {
        this->zoom = l_zoom;

        double res = merc_max_resolution / double(1 << this->zoom);

        this->x = l_google_url_x;
        // flip Y value - the URLs we use are Google URLs (tms_type='google' in
        // the terminology of tilecache), but internally we use the Tile Map
        // Service Specification
        // (http://wiki.osgeo.org/wiki/Tile_Map_Service_Specification)
        // convention. i.e. Y increases as you head North.
        int max_url_y = int(round( (merc_y_orig_max - merc_y_orig_min) / (res * IMAGE_HEIGHT))) - 1;
        this->y = max_url_y - l_google_url_y;

        this->min_x_merc = merc_x_orig_min + (res * this->x * IMAGE_WIDTH);
        this->min_y_merc = merc_y_orig_min + (res * this->y * IMAGE_HEIGHT);
        this->max_x_merc = merc_x_orig_min + (res * (this->x + 1) * IMAGE_WIDTH);
        this->max_y_merc = merc_y_orig_min + (res * (this->y + 1) * IMAGE_HEIGHT);

        this->pixels_per_meter = this->calc_pixels_per_meter();
    }

    // Convert a mercator coordinate into a pixel coordinate on the tile
    // XXX could output doubles here for accuracy for other purposes
    void transform_merc_onto_tile(double merc_x, double merc_y, int& tile_x, int &tile_y) const {
        tile_x = (merc_x - min_x_merc) / (max_x_merc - min_x_merc) * IMAGE_WIDTH;
        tile_y = (merc_y - min_y_merc) / (max_y_merc - min_y_merc) * IMAGE_HEIGHT;
    }

    // Convert pixel coordinate on a tile into a mercator coordinate
    void transform_tile_onto_merc(int tile_x, int tile_y, double& merc_x, double& merc_y) const {
        merc_x = (double(tile_x) / double(IMAGE_WIDTH)) * (max_x_merc - min_x_merc) + min_x_merc;
        merc_y = (double(tile_y) / double(IMAGE_HEIGHT)) * (max_y_merc - min_y_merc) + min_y_merc;
    }

    // Test to see if a mercator coordinate is on the tile or not.
    bool is_merc_on_tile(double merc_x, double merc_y) const {
        return (merc_x >= this->min_x_merc) &&
            (merc_x <= this->max_x_merc) &&
            (merc_y >= this->min_y_merc) &&
            (merc_y <= this->max_y_merc);
    }
    
    // Test to see if a pixel coordinate on the tile is within box extended
    // in both dimensions by distance pixels of the tile.
    bool is_pixel_near_tile(int x, int y, int distance) const {
        return (x >= -distance && x <= IMAGE_WIDTH + distance &&
                y >= -distance && y <= IMAGE_HEIGHT + distance);
    }

    std::string debug_info() {
        return (boost::format("Tile: zoom/x/y: %d/%d/%d merc-x-range: %lf %lf merc-y-range: %lf %lf pixels/m: %lf") % this->zoom % this->x % this->y % min_x_merc % max_x_merc % min_y_merc % max_y_merc % this->pixels_per_meter).str();
    }

    // Number of pixels per meter of spherical globe in current projection.
    double calc_pixels_per_meter() const {
        double lon1, lat1;
        double lon2, lat2;
        merc_to_lat_lon(this->min_x_merc, this->min_y_merc, &lat1, &lon1);
        merc_to_lat_lon(this->max_x_merc, this->max_y_merc, &lat2, &lon2);
        //debug_log(boost::format("pixels_per_meter: internal lat1 lon1 %lf %lf") % lat1 % lon1);
        //debug_log(boost::format("pixels_per_meter: internal lat2 lon2 %lf %lf") % lat2 % lon2);

        double diagonal_1_in_m = great_circle_distance(lat1, lon1, lat2, lon2);
        double diagonal_2_in_m = great_circle_distance(lat1, lon2, lat2, lon1);
        double average_diagonal_in_m = (diagonal_1_in_m + diagonal_2_in_m) / 2;
        //debug_log(boost::format("pixels_per_meter: internal diagonal_1_in_m diagonal_2_in_m %lf %lf") % diagonal_1_in_m % diagonal_2_in_m);

        return image_diagonal / average_diagonal_in_m;
    }

    // Convert a distance in meters to an approximate distance in pixels on the tile
    double meters_to_pixels(double distance) const {
        double pixels = distance * this->pixels_per_meter;
        return pixels;
    }

    int zoom;
    int x, y;

    double min_x_merc, max_x_merc;
    double min_y_merc, max_y_merc;

    double pixels_per_meter;
};

/////////////////////////////////////////////////////////////////////
// Data sets - storing and indexing

// A datum stores an item of the input data set. Has a coordinate, and data
// value. The data value will, for example, be journey time, house price, wind
// speed.
class Datum {
    public:
    // x, y are in spherical mercator coordinates
    double x;
    double y;
    // value is in implementation dependent units 
    double value;
    Datum(double x, double y, double value) {
        this->x = x;
        this->y = y;
        this->value = value;
    }
};

// A data set is the data behind a particular layer. e.g. All the house prices used.
typedef std::vector<Datum> DatumEntries;
typedef unsigned int DatumIndex;
typedef std::list<DatumIndex> DatumIndexList;
typedef std::vector< std::vector< DatumIndexList > > DatumBoxSet;
class DataSet {
    public:
    DatumEntries entries;

    DataSet() {
        this->x_min = DBL_MAX;
        this->y_min = DBL_MAX;
        this->x_max = DBL_MIN;
        this->y_max = DBL_MIN;
    }

    // add a new point to data set, keeping boundaries up to date
    Datum& add_datum(double x, double y, double value) {
        this->entries.push_back(Datum(x, y, value));
        if (x > this->x_max)
            this->x_max = x;
        if (x < this->x_min)
            this->x_min = x;
        if (y > this->y_max)
            this->y_max = y;
        if (y < this->y_min)
            this->y_min = y;
        // debug_log(boost::format("add_datum x y: %lf %lf value: %lf") % x % y % value);
        return this->entries[this->entries.size() - 1];
    }

    // display basic information about data set
    std::string debug_info() {
        return (boost::format("DataSet: Number of datums: %d X-Range: %lf %lf Y-Range: %lf %lf") % this->entries.size() % this->x_min % this->x_max % this->y_min % this->y_max).str();
    }

    // return parameter value
    double get_param(const std::string& name) const {
        return this->params.find(name)->second;
    }

    // ranges allowed for datum locations
    double x_min, x_max; 
    double y_min, y_max;

    // other parameters for rendering the data set
    std::map<std::string, double> params;

    // used to quickly find datums
    double box_set_radius;
    int box_set_width, box_set_height;
    DatumBoxSet box_set;
};

// Create a grid of squares, each datum going into one squares. Squares are same size
// as the maximum radius that a datum can affect the tile colour.
void datum_box_set_make(DataSet& data_set, double radius) {
    DatumBoxSet& box_set = data_set.box_set;
    box_set.clear();
    data_set.box_set_radius = radius;

    // work out how many entries there are in the box set
    int box_set_width = int((data_set.x_max - data_set.x_min) / data_set.box_set_radius) + 1;
    int box_set_height = int((data_set.y_max - data_set.y_min) / data_set.box_set_radius) + 1;
    box_set.resize(box_set_width);
    data_set.box_set_width = box_set_width;
    data_set.box_set_height = box_set_height;
    // ... allocate storage
    for (DatumBoxSet::iterator it = box_set.begin(); it != box_set.end(); it++) {
        it->resize(box_set_height);
    }

    // put each datum within its box
    for (DatumIndex ix = 0; ix < data_set.entries.size(); ix++) {
        const Datum& datum = data_set.entries[ix];

        assert(datum.x >= data_set.x_min);
        assert(datum.x <= data_set.x_max);
        assert(datum.y >= data_set.y_min);
        assert(datum.y <= data_set.y_max);

        int box_x = int((datum.x - data_set.x_min) / data_set.box_set_radius);
        int box_y = int((datum.y - data_set.y_min) / data_set.box_set_radius);

        assert(box_x >= 0);
        assert(box_x < box_set_width);
        assert(box_y >= 0);
        assert(box_y < box_set_height);

        DatumIndexList &datum_index_list = box_set[box_x][box_y];
        datum_index_list.push_back(ix);
    }
}
// Given a point (a datum, essentially), return the position of the box set grid cell that contains that point.
void datum_box_set_square_at_point(const DataSet& data_set, const double x, const double y, int& box_x, int& box_y) {
    box_x = int((x - data_set.x_min) / data_set.box_set_radius);
    box_y = int((y - data_set.y_min) / data_set.box_set_radius);
    // make sure it is in bounds
    if (box_x < 0) box_x = 0;
    if (box_x >= data_set.box_set_width) box_x = data_set.box_set_width - 1;
    if (box_y < 0) box_y = 0;
    if (box_y >= data_set.box_set_height) box_y = data_set.box_set_height - 1;
}
// Returns all the datums in the given (mercator coordinate) rectangle.
void datum_box_set_find_by_rectangle(const DataSet& data_set, const double x_1, const double y_1, const double x_2, const double y_2, DatumIndexList &ret) {
    int box_x_1, box_y_1;
    datum_box_set_square_at_point(data_set, x_1, y_1, box_x_1, box_y_1);
    int box_x_2, box_y_2;
    datum_box_set_square_at_point(data_set, x_2, y_2, box_x_2, box_y_2);

    debug_log((boost::format("datum_box_set_find_by_rectangle: found ranges: box x: %d %d box y: %d %d ") % box_x_1 % box_x_2 % box_y_1 % box_y_2).str());

    ret.clear();
    for (int box_x = box_x_1; box_x <= box_x_2; box_x++) {
        for (int box_y = box_y_1; box_y <= box_y_2; box_y++) {
            const DatumIndexList &datum_index_list = data_set.box_set[box_x][box_y];
            for (DatumIndexList::const_iterator it = datum_index_list.begin(); it != datum_index_list.end(); it++) {
                DatumIndex ix = *it;
                ret.push_back(ix);
            }
        }
    }
}

// Draw a test pattern on the tile
void draw_pretty_test_pattern() {
    int d = 0;
    for (int x = 0; x < IMAGE_WIDTH; x++) {
        for (int y = 0; y < IMAGE_HEIGHT; y++) {
            guarded_plot(x, y, d);
            d++;
        }
    }

}

/////////////////////////////////////////////////////////////////////
// Drawing functions

// Draw some inverted cones on the tile. The cones are inverted, with their point
// at the bottom. The height of the point is the value of the datum, its centre
// point is the position of the datum. The height is used as the colour value of
// the pixel. When two cones are drawn on top of each other, the minimum height
// is used. This algorithm is, for example, used for making contours of travel
// time by public transport.
void draw_datums_as_cones_loop_by_datum(const DataSet& data_set, const Tile& tile) {
    double max_walk_distance_in_meters = data_set.get_param("max_walk_distance_in_meters");
    double max_walk_time = data_set.get_param("max_walk_time");
    double pixel_radius = tile.meters_to_pixels(max_walk_distance_in_meters);
    int int_pixel_radius = int(pixel_radius) + 1;
    debug_log(boost::format("draw_datums_as_cones_loop_by_datum: max_walk_distance_in_meters %lf max_walk_time %lf pixel_radius %lf") % max_walk_distance_in_meters % max_walk_time % pixel_radius);

    // Work out which datums might matter, using box set
    DatumIndexList datum_index_list;
    double x_1, y_1;
    tile.transform_tile_onto_merc(-int_pixel_radius, -int_pixel_radius, x_1, y_1);
    double x_2, y_2;
    tile.transform_tile_onto_merc(IMAGE_WIDTH + int_pixel_radius, IMAGE_HEIGHT + int_pixel_radius, x_2, y_2);
    datum_box_set_find_by_rectangle(data_set, x_1, y_1, x_2, y_2, datum_index_list);
    debug_log(boost::format("draw_datums_as_cones_loop_by_datum: datum count %d datums nearby %d") % data_set.entries.size() % datum_index_list.size());

    for (DatumIndexList::const_iterator it = datum_index_list.begin(); it != datum_index_list.end(); it++) {
        DatumIndex ix = *it;
        const Datum& datum = data_set.entries[ix];
        int datum_on_tile_x, datum_on_tile_y;
    
        // Do finer grained clipping than box set does - 
        // XXX perhaps instead call this in datum_box_set_find_by_rectangle?
        tile.transform_merc_onto_tile(datum.x, datum.y, datum_on_tile_x, datum_on_tile_y);
        if (!tile.is_pixel_near_tile(datum_on_tile_x, datum_on_tile_y, pixel_radius)) {
            continue;
        }

        //if (datum_on_tile_x > 0 && datum_on_tile_y > 0 && datum_on_tile_x < IMAGE_WIDTH && datum_on_tile_y < IMAGE_HEIGHT)
        //    debug_log(boost::format("datum merc: %lf %lf datum tile place: %d %d value: %d") % datum.x % datum.y % datum_on_tile_x % datum_on_tile_y %datum.value);
       
        // Clip the cone
        int loop_x_min, loop_x_max;
        loop_x_min = std::max(datum_on_tile_x - int_pixel_radius, 0);
        loop_x_max = std::min(datum_on_tile_x + int_pixel_radius, IMAGE_WIDTH);
        int loop_y_min, loop_y_max;
        loop_y_min = std::max(datum_on_tile_y - int_pixel_radius, 0);
        loop_y_max = std::min(datum_on_tile_y + int_pixel_radius, IMAGE_HEIGHT);
        // Loop over pixels of cone, rendering into place
        for (int plot_x = loop_x_min; plot_x <= loop_x_max; plot_x++) {
            for (int plot_y = loop_y_min; plot_y <= loop_y_max; plot_y++) {
                int x = plot_x - datum_on_tile_x;
                int y = plot_y - datum_on_tile_y;
                double dist = calc_dist_fast_int_on_tile(int(x), int(y));
                if (dist <= pixel_radius) {
                    // debug_log(boost::format("dist: %lf pixel_radius: %lf") % dist % pixel_radius);
                    guarded_min_plot(plot_x, plot_y, dist / pixel_radius * max_walk_time + datum.value);
                }
            }
        }

    }
}

// Efficient version of draw_datums_as_cones_loop_by_datum, which loops over pixels
// rather than over cones.
void draw_datums_as_cones_loop_by_pixel(const DataSet& data_set, const Tile& tile) {
    double max_walk_distance_in_meters = data_set.get_param("max_walk_distance_in_meters");
    double max_walk_time = data_set.get_param("max_walk_time");
    double pixel_radius = tile.meters_to_pixels(max_walk_distance_in_meters);
    int int_pixel_radius = int(pixel_radius) + 1;
    debug_log(boost::format("draw_datums_as_cones_loop_by_pixel: max_walk_distance_in_meters %lf max_walk_time %lf pixel_radius %lf") % max_walk_distance_in_meters % max_walk_time % pixel_radius);

    double pixel_radius_sq = pixel_radius * pixel_radius;

    // Work out which datums might matter
    DatumIndexList datum_index_list;
    double x_1, y_1;
    tile.transform_tile_onto_merc(-int_pixel_radius, -int_pixel_radius, x_1, y_1);
    double x_2, y_2;
    tile.transform_tile_onto_merc(IMAGE_WIDTH + int_pixel_radius, IMAGE_HEIGHT + int_pixel_radius, x_2, y_2);
    datum_box_set_find_by_rectangle(data_set, x_1, y_1, x_2, y_2, datum_index_list);
    debug_log(boost::format("draw_datums_as_cones_loop_by_pixel: datum count %d datums nearby %d") % data_set.entries.size() % datum_index_list.size());

    for (int x = 0; x < IMAGE_WIDTH; x++) {
        for (int y = 0; y < IMAGE_HEIGHT; y++) {
            //debug_log(boost::format("draw_datums_as_cones_loop_by_pixel: x: %d y: %d") % x % y);

            double min_dist = -1;
            double min_value = -1;

            for (DatumIndexList::const_iterator it = datum_index_list.begin(); it != datum_index_list.end(); it++) {
                DatumIndex ix = *it;
                const Datum& datum = data_set.entries[ix];

                int datum_on_tile_x, datum_on_tile_y;
                tile.transform_merc_onto_tile(datum.x, datum.y, datum_on_tile_x, datum_on_tile_y);
                if (!tile.is_pixel_near_tile(datum_on_tile_x, datum_on_tile_y, pixel_radius)) {
                    continue;
                }

                // Find relative position of datum from the pixel we are plotting
                int rel_x = datum_on_tile_x - x;
                int rel_y = datum_on_tile_y - y;
                double dist_sq = calc_dist_sq(rel_x, rel_y);
                if (dist_sq <= pixel_radius_sq) {
                    //debug_log(boost::format("draw_datums_as_cones_loop_by_pixel: rel_x: %d rel_y: %d dist_sq: %lf pixel_radius_sq: %lf") % rel_x % rel_y % dist_sq % pixel_radius_sq);
                    double dist = calc_dist_fast_int_anywhere(rel_x, rel_y);
                    double value = dist / pixel_radius * max_walk_time + datum.value;
                    if (min_dist < 0 || value < min_value) {
                        min_dist = dist;
                        min_value = value;
                    }
                }
            }

            if (min_dist >= 0) {
                guarded_plot(x, y, min_value);
            } else {
                guarded_plot(x, y, no_data_colour);
            }
        }
    }
}

/////////////////////////////////////////////////////////////////////
// Main entry point

int main(int argc, char * argv[]) {
    PerformanceMonitor pm;
    DataSet data_set;

    /*
    double mercx, mercy;
    lat_lon_to_merc(53.466667, -2.233333, &mercx, &mercy); // Manchester
    printf("Manchester mercx, mercy: %lf %lf\n", mercx, mercy); // roughly: -248128.680454, 7071667.54412 (that's actually Manchester Picadilly)
    double lat, lon;
    merc_to_lat_lon(-248613.492332, 7069789.545191, &lat, &lon); // Manchester
    printf("Manchester lat, lon: %lf %lf\n", lat, lon); // 53.466667, -2.233333
    */

    /*if (argc < 7) {
        fprintf(stderr, "fastplan.cpp arguments are:\n  1. fast index file prefix\n  2. output prefix (or 'stream' for stdout incremental)\n  3. arrive_by or depart_after\n  4. target arrival time / departure in mins after midnight\n  5. target location\n  6. earliest/latest departure in mins after midnight to go back to\n  7, 8. easting, northing to use to find destination if destination is 'coordinate'\n");
        return 1;
    }*/
    
    // Precalculate some things for optimisation
    calc_dist_fast_int_initialise();
    pm.display("Precalculating square roots took");

    // Read data set from .nodes file
    std::string nodes_file = "/home/francis/toobig/nptdr/tmpwork/test.nodes";
    std::string iso_file = "/home/francis/toobig/nptdr/tmpwork/1440.iso";
    struct stat nodes_info;
    stat(nodes_file.c_str(), &nodes_info);
    int nodes_to_read = nodes_info.st_size / sizeof(double) / 2;
    if (stat < 0) {
        throw Exception("failed to stat .nodes file");
    }
    FILE *nodes_h = fopen(nodes_file.c_str(), "rb");
    if (nodes_h < 0) {
        throw Exception("failed to fopen .nodes file");
    }
    FILE *iso_h = fopen(iso_file.c_str(), "rb");
    if (iso_h < 0) {
        throw Exception("failed to fopen .iso file");
    }
    for (int i = 0; i < nodes_to_read; ++i) {
        double x, y;
        my_fread(&x, 1, sizeof(double), nodes_h);
        my_fread(&y, 1, sizeof(double), nodes_h);
        short int value;
        my_fread(&value, 1, sizeof(short int), iso_h);
        if (i > 0) { // XXX skip station 0 for now
            if (value >= 0) { // -1 is no journey available
                data_set.add_datum(x, y, value * 60); // file contains minutes, plotting uses seconds
            }
        }
    }
    data_set.params["max_walk_distance_in_meters"] = 2400; // 2400 meters is a half hour of walking at 1.33333 m/s
    data_set.params["max_walk_time"] = 1800; // 1800 seconds is half an hour 

    // Internal test populate data set
    /*
    int c = 0;
    for (int i = 3; i < 10; i++) {
        for (int j = 3; j < 10; j++) {
            c++;
            data_set.add_datum(i * 24, j * 24, c * 5);
        }
    }
    */

    pm.display("Initialising data set took");
    datum_box_set_make(data_set, 1000); // XXX 1000 is just a guess an boxset optimisation parameter
    pm.display("Making box set took");
    debug_log(data_set.debug_info());

    // Work out which tile to go for 
    // XXX these tile_ would come from the URL e.g. iso/11/1011/671.png
    Tile tile(11, 1011, 671); // zoom, x, y as in URL, e.g. iso/11/1011/671.png
    debug_log(tile.debug_info());

    // Create gd image surface
    im = gdImageCreateTrueColor(IMAGE_WIDTH, IMAGE_HEIGHT);
    int white = gdImageColorAllocate(im, 255, 255, 255);  
    gdImageFilledRectangle(im, 0, 0, IMAGE_WIDTH, IMAGE_HEIGHT, white);
    pm.display("Creating surface took");

    // Set pixel values
    //draw_pretty_test_pattern();
    draw_datums_as_cones_loop_by_datum(data_set, tile);
    //draw_datums_as_cones_loop_by_pixel(data_set, tile);
    debug_log(boost::format("Plot count: %d Squareroot count: %d") % plot_count % sqrt_count);
    pm.display("Plotting image took");

    // Write out PNG file
    FILE *out = fopen ("/tmp/drawtile.png", "wb");
    gdImagePngEx(im, out, -1); // -1 is default compression, 0 is no compression
    fclose(out);
    pm.display("Writing PNG took");
}


