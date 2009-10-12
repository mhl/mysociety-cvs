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
// $Id: drawtile.cpp,v 1.23 2009-10-12 23:01:41 francis Exp $
//

// TODO:
// Move im to be member of Tile?

#include <math.h> 
#include <gd.h>
#include <assert.h>
#include <float.h>

#include <sys/types.h>
#include <sys/stat.h>

#include <vector>
#include <list>
#include <map>
#include <set>
#include <algorithm>
#include <fcgiapp.h>

#include <boost/foreach.hpp>

#include "../../cpplib/mysociety_error.h"
#include "../../cpplib/mysociety_geo.h"
#include "../../cpplib/performance_monitor.h"

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

/* Optimised version of length of vector. Only takes pixel lengths which are
 * shorter than the given sizeas input, caches results for output. */
#define SQRT_CACHE_X_MAX IMAGE_WIDTH + 100 // will only work for zoom levels where pixel radius is < 100
#define SQRT_CACHE_Y_MAX IMAGE_HEIGHT + 100
double sqrt_cache_sum[SQRT_CACHE_X_MAX+1][SQRT_CACHE_Y_MAX+1];
double sqrt_cache_sub[SQRT_CACHE_X_MAX+1][SQRT_CACHE_Y_MAX+1];
bool sqrt_cache_initialised = false;
void calc_dist_fast_int_initialise() {
    for (int x = 0; x <= SQRT_CACHE_X_MAX; x++) {
        for (int y = 0; y <= SQRT_CACHE_Y_MAX; y++) {
            sqrt_cache_sum[x][y] = sqrt(double(x * x + y * y));
            if (x >= y) {
                sqrt_cache_sub[x][y] = sqrt(double(x * x - y * y));
            }
        }
    }

    sqrt_cache_initialised = true;
}
double calc_dist_fast_int_sum(int x, int y) {
    // debug_log(boost::format("calc_dist_fast_int_sum: %d %d") % x % y);
    x = x > 0 ? x : -x;
    y = y > 0 ? y : -y;

    assert(x >= 0 && y >= 0 && x <= SQRT_CACHE_X_MAX && y <= SQRT_CACHE_Y_MAX);
    assert(sqrt_cache_initialised);

    double result = sqrt_cache_sum[x][y];
    return result;
}
double calc_dist_fast_int_sub(int x, int y) {
    // debug_log(boost::format("calc_dist_fast_int_sub: %d %d") % x % y);
    x = x > 0 ? x : -x;
    y = y > 0 ? y : -y;

    assert (x >= y);
    assert(x >= 0 && y >= 0 && x <= SQRT_CACHE_X_MAX && y <= SQRT_CACHE_Y_MAX);
    assert(sqrt_cache_initialised);

    double result = sqrt_cache_sub[x][y];
    return result;
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

/* Plot a pixel on a tile, check values in range, but use the minimum value 
 * See guarded_plot above for reason why we flip the Y value just before drawing. */
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
        // flip Y value - the URLs we use are Google Maps URLs
        // (tms_type='google' in the terminology of tilecache), but internally
        // we use the Tile Map Service Specification
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

    // Static function that returns the Google Maps style URL which contains a
    // given mercator point at a given zoom.
    static void merc_to_google_url(double merc_x, double merc_y, int zoom, int& google_url_x, int&google_url_y) {
        double res = merc_max_resolution / double(1 << zoom);
        double x = (merc_x - merc_x_orig_min) / res / IMAGE_WIDTH;
        double y = (merc_y - merc_y_orig_min) / res / IMAGE_WIDTH;

        google_url_x = (int)x;
        int max_url_y = int(round( (merc_y_orig_max - merc_y_orig_min) / (res * IMAGE_HEIGHT))) - 1;
        google_url_y = max_url_y - (int)y;
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
        debug_log(boost::format("pixels_per_meter: internal merc %lf %lf lat1 lon1 %lf %lf") % this->min_x_merc % this->min_y_merc % lat1 % lon1);
        debug_log(boost::format("pixels_per_meter: internal merc %lf %lf lat2 lon2 %lf %lf") % this->max_x_merc % this->max_y_merc % lat2 % lon2);

        double diagonal_1_in_m = great_circle_distance(lat1, lon1, lat2, lon2);
        double diagonal_2_in_m = great_circle_distance(lat1, lon2, lat2, lon1);
        double average_diagonal_in_m = (diagonal_1_in_m + diagonal_2_in_m) / 2;
        debug_log(boost::format("pixels_per_meter: internal diagonal_1_in_m diagonal_2_in_m %lf %lf") % diagonal_1_in_m % diagonal_2_in_m);

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
typedef std::vector<DatumIndex> DatumIndexList;
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
    std::string get_param(const std::string& name) const {
        return this->params.find(name)->second;
    }
    double get_param_double(const std::string& name) const {
        return atof(this->params.find(name)->second.c_str());
    }
    int get_param_int(const std::string& name) const {
        return atoi(this->params.find(name)->second.c_str());
    }

    // ranges allowed for datum locations
    double x_min, x_max; 
    double y_min, y_max;

    // other parameters for rendering the data set
    std::map<std::string, std::string> params;

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

    debug_log((boost::format("box set width: %d height: %d") % box_set_width % box_set_height).str());
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

    //debug_log((boost::format("datum_box_set_find_by_rectangle: found ranges: box x: %d %d box y: %d %d ") % box_x_1 % box_x_2 % box_y_1 % box_y_2).str());

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

/////////////////////////////////////////////////////////////////////
// Drawing functions - cones

// Draw some inverted cones on the tile. The cones are inverted, with their point
// at the bottom. The height of the point is the value of the datum, its centre
// point is the position of the datum. The height is used as the colour value of
// the pixel. When two cones are drawn on top of each other, the minimum height
// is used. This algorithm is, for example, used for making contours of travel
// time by public transport.
void draw_datums_as_cones_loop_by_datum(const DataSet& data_set, const Tile& tile) {
    double max_walk_distance_in_meters = data_set.get_param_double("max_walk_distance_in_meters");
    double max_walk_time = data_set.get_param_double("max_walk_time");
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

    int inner_count = 0;
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
       
        // Clip the cone in X direction
        int loop_x_min, loop_x_max;
        loop_x_min = std::max(datum_on_tile_x - int_pixel_radius, 0);
        loop_x_max = std::min(datum_on_tile_x + int_pixel_radius, IMAGE_WIDTH);
        // Loop over pixels of cone, rendering into place
        for (int plot_x = loop_x_min; plot_x <= loop_x_max; plot_x++) {
            int x = plot_x - datum_on_tile_x;
            // Work out range to use in Y direction (to make circular cone, clipped to tile)
            int y_max = int(calc_dist_fast_int_sub(int_pixel_radius, x)) + 1;
            int loop_y_min, loop_y_max;
            loop_y_min = std::max(datum_on_tile_y - y_max, 0);
            loop_y_max = std::min(datum_on_tile_y + y_max, IMAGE_HEIGHT);
            //    debug_log(boost::format("y_max is: %d pixel_radius is: %d") % y_max % pixel_radius);
            //
            for (int plot_y = loop_y_min; plot_y <= loop_y_max; plot_y++) {
                int y = plot_y - datum_on_tile_y;
                inner_count++;
                double dist = calc_dist_fast_int_sum(int(x), int(y));
                guarded_min_plot(plot_x, plot_y, dist / pixel_radius * max_walk_time + datum.value);
            }
        }

    }

    debug_log(boost::format("inner_count %d") % inner_count);
}

// Alternative version of draw_datums_as_cones_loop_by_datum, which loops over
// pixels rather than over cones. Hoped it would be quicker, but it isn't.
void draw_datums_as_cones_loop_by_pixel(const DataSet& data_set, const Tile& tile) {
    double max_walk_distance_in_meters = data_set.get_param_double("max_walk_distance_in_meters");
    double max_walk_time = data_set.get_param_double("max_walk_time");
    double pixel_radius = tile.meters_to_pixels(max_walk_distance_in_meters);
    int int_pixel_radius = int(pixel_radius) + 1;
    debug_log(boost::format("draw_datums_as_cones_loop_by_pixel: max_walk_distance_in_meters %lf max_walk_time %lf pixel_radius %lf") % max_walk_distance_in_meters % max_walk_time % pixel_radius);

    double pixel_radius_sq = pixel_radius * pixel_radius;

    // Work out which datums might matter, using box set
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
            DatumIndex min_ix = -1;

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
                    double dist = calc_dist_fast_int_sum(rel_x, rel_y);
                    double value = dist / pixel_radius * max_walk_time + datum.value;
                    if (min_dist < 0 || value < min_value) {
                        min_dist = dist;
                        min_value = value;
                        min_ix = ix;
                    }
                }
            }

            if (min_dist >= 0) {
                //guarded_plot(x, y, min_value);
                guarded_plot(x, y, min_ix * 200);
            } else {
                guarded_plot(x, y, no_data_colour);
            }
        }
    }
}

// Class representing the values of *every* cone's height at a particular position.
class ConeValuesAtPoint {
    public:
    int drop_x, drop_y;
    typedef std::pair<double, DatumIndex> ValueDatumPair;
    std::vector< ValueDatumPair > rlist;

    // Constructor which calculates the values of *all* the cones at the tile position drop_x, drop_y
    ConeValuesAtPoint(const DataSet& data_set, const Tile& tile, const DatumIndexList& datum_index_list, int drop_x, int drop_y, double pixel_radius, double max_walk_time) {
        this->drop_x = drop_x;
        this->drop_y = drop_y;

        for (DatumIndexList::const_iterator it = datum_index_list.begin(); it != datum_index_list.end(); it++) {
            DatumIndex ix = *it;
            const Datum& datum = data_set.entries[ix];

            int datum_on_tile_x, datum_on_tile_y;
            tile.transform_merc_onto_tile(datum.x, datum.y, datum_on_tile_x, datum_on_tile_y);
            if (!tile.is_pixel_near_tile(datum_on_tile_x, datum_on_tile_y, pixel_radius)) {
                continue;
            }

            // Find relative position of datum from the pixel we are plotting
            double dist = calc_dist_fast_int_sum(datum_on_tile_x - drop_x, datum_on_tile_y - drop_y);
            double value = dist / pixel_radius * max_walk_time + datum.value;
            this->rlist.push_back(ValueDatumPair(value, ix));
        }

        // Sort them, the lowest first.
        std::sort(this->rlist.begin(), this->rlist.end());

        /*for (unsigned int i = 0; i < this->rlist.size(); ++i) {
            debug_log(boost::format("cone value: %lf") % this->rlist[i].first);
        }*/
    }

    // Calculate value at x, y - scan fewer datums by using the values calculated in the constructor.
    double evaluate_min_at_point(const DataSet& data_set, const Tile& tile, int x, int y, double pixel_radius, double max_walk_time) {
        // How far in time from the drop point are we?
        double dist_drop_to_point = calc_dist_fast_int_sum(this->drop_x - x, this->drop_y - y);
        double time_dist_drop_to_point = dist_drop_to_point / pixel_radius * max_walk_time;
        // The lowest cone at the drop point, will likely still be lowest in nearby areas. 
        // The only other cones that can have gone below it, must be within twice the walking
        // time between. This is because:
        // i) the rate of change of any hyperbolic slice of the cone is at most the walking
        // speed (i.e. the rate of change of the hyperbolic slice through the centre of the one)
        // ii) the lowest cone can have risen up most the walking time, and the other cones
        // can have gone down by at most the walking time. Making twice walking time in total.
        double max_r = -1;
        if (rlist.size() > 0) {
            max_r = rlist.front().first + (2 * time_dist_drop_to_point);
        }

        double min_value = -1;
        for (unsigned int i = 0; i < this->rlist.size(); ++i) {
            ValueDatumPair p = rlist[i];
            double drop_value = p.first;
            DatumIndex ix = p.second;
            const Datum& datum = data_set.entries[ix];

            // drop out if we are too far
            if (max_r != -1 && drop_value > max_r) {
                //debug_log(boost::format("jumping out drop-value: %lf max_r: %lf") % drop_value % max_r);
                break;
            }

            // work out value for this cone at our pixel position
            int datum_on_tile_x, datum_on_tile_y;
            tile.transform_merc_onto_tile(datum.x, datum.y, datum_on_tile_x, datum_on_tile_y);
            double dist_sq = calc_dist_sq(datum_on_tile_x - x, datum_on_tile_y - y);
            double compare_against = (min_value - datum.value) * pixel_radius / max_walk_time;
            // This squared comparison is equivalent to the following, only leaves the squareroot until later
            // if (min_value == -1 || value < min_value) {
            if (min_value == -1 || dist_sq < compare_against * compare_against) {
                double dist = calc_dist_fast_int_sum(datum_on_tile_x - x, datum_on_tile_y - y);
                double value = dist / pixel_radius * max_walk_time + datum.value;
                if (min_value != -1 && value > min_value) {
                    debug_log(boost::format("error value > min_value %lf >= %lf") % value % min_value);
                }

                min_value = value;
                // update our max limit, as we now know how far up the lower cones have come
                max_r = min_value + time_dist_drop_to_point;
            }
        }
        return min_value;
    }
};

void draw_datums_as_cones_with_drop_line(const DataSet& data_set, const Tile& tile) {
    double max_walk_distance_in_meters = data_set.get_param_double("max_walk_distance_in_meters");
    double max_walk_time = data_set.get_param_double("max_walk_time");
    double pixel_radius = tile.meters_to_pixels(max_walk_distance_in_meters);
    int int_pixel_radius = int(pixel_radius) + 1;
    debug_log(boost::format("draw_datums_as_cones_with_drop_line: max_walk_distance_in_meters %lf max_walk_time %lf pixel_radius %lf") % max_walk_distance_in_meters % max_walk_time % pixel_radius);

    // Work out which datums might matter, using box set
    DatumIndexList datum_index_list;
    double x_1, y_1;
    tile.transform_tile_onto_merc(-int_pixel_radius, -int_pixel_radius, x_1, y_1);
    double x_2, y_2;
    tile.transform_tile_onto_merc(IMAGE_WIDTH + int_pixel_radius, IMAGE_HEIGHT + int_pixel_radius, x_2, y_2);
    datum_box_set_find_by_rectangle(data_set, x_1, y_1, x_2, y_2, datum_index_list);
    debug_log(boost::format("draw_datums_as_cones_with_drop_line: datum count %d datums nearby %d") % data_set.entries.size() % datum_index_list.size());

    // Loop in a subtiles of DROP_STEP size over the tile
    int DROP_STEP = 16;
    for (unsigned int drop_x = 0; drop_x < IMAGE_WIDTH; drop_x += DROP_STEP) {
        for (unsigned int drop_y = 0; drop_y < IMAGE_HEIGHT; drop_y += DROP_STEP) {
            // Drop a line - i.e. calculate the values of all datum cones - at the centre of the subtile
            ConeValuesAtPoint vlap(data_set, tile, datum_index_list, drop_x + DROP_STEP / 2, drop_y + DROP_STEP / 2, pixel_radius, max_walk_time);
            // Loop over each pixel of the subtile
            for (unsigned int x = drop_x; x < drop_x + DROP_STEP; x += 1) {
                //debug_log(boost::format("draw_datums_as_cones_with_drop_line: x: %d") % x);
                for (unsigned int y = drop_y; y < drop_y + DROP_STEP; y += 1) {
                    
                    // Using dropped line to limit cones that could have effected it, plot point
                    double min_value = vlap.evaluate_min_at_point(data_set, tile, x, y, pixel_radius, max_walk_time);
                    if (min_value >= 0) {
                        guarded_plot(x, y, min_value);
                        //guarded_plot(x, y, min_ix * 200);
                    } else {
                        guarded_plot(x, y, no_data_colour);
                    }
                }
            }

        }
    }
}

/////////////////////////////////////////////////////////////////////
// Drawing functions - median

// Find median of values within a given radius from each pixel.
// Chris Lightfoot used a median algorithm for house prices in his original protoype, with:
//    1km search radius
//    10 minimum points (otherwise returns no data)
void draw_datums_as_median_naive(const DataSet& data_set, const Tile& tile) {
    double search_radius_in_meters = data_set.get_param_double("search_radius_in_meters");
    int minimum_points = data_set.get_param_int("minimum_points");
    if (minimum_points < 1)
        minimum_points = 1;
    double pixel_radius = tile.meters_to_pixels(search_radius_in_meters);
    int int_pixel_radius = int(pixel_radius) + 1;
    debug_log(boost::format("draw_datums_as_median_naive: search_radius_in_meters %lf pixel_radius %lf") % search_radius_in_meters % pixel_radius);

    double pixel_radius_sq = pixel_radius * pixel_radius;

    DatumIndexList datum_index_list;
    for (int x = 0; x < IMAGE_WIDTH; x++) {
        for (int y = 0; y < IMAGE_HEIGHT; y++) {
            //debug_log(boost::format("draw_datums_as_cones_loop_by_pixel: x: %d y: %d") % x % y);

            // Work out which datums might matter
            datum_index_list.clear();
            double x_1, y_1;
            tile.transform_tile_onto_merc(x - int_pixel_radius, y - int_pixel_radius, x_1, y_1);
            double x_2, y_2;
            tile.transform_tile_onto_merc(x + int_pixel_radius, y + int_pixel_radius, x_2, y_2);
            datum_box_set_find_by_rectangle(data_set, x_1, y_1, x_2, y_2, datum_index_list);
            //debug_log(boost::format("draw_datums_as_median_naive: datum count %d datums nearby %d") % data_set.entries.size() % datum_index_list.size());

            std::vector<double> value_list;
            for (DatumIndexList::const_iterator it = datum_index_list.begin(); it != datum_index_list.end(); it++) {
                DatumIndex ix = *it;
                const Datum& datum = data_set.entries[ix];
                int datum_on_tile_x, datum_on_tile_y;
                tile.transform_merc_onto_tile(datum.x, datum.y, datum_on_tile_x, datum_on_tile_y);
                double dist_sq = calc_dist_sq(datum_on_tile_x - x, datum_on_tile_y - y);
                if (dist_sq <= pixel_radius_sq) {
                    value_list.push_back(datum.value);
                }
            }

            if ((int)value_list.size() >= minimum_points) {
                // For discussion of quickly finding medians in C++ see
                // http://stackoverflow.com/questions/810657/fastest-code-c-c-to-select-the-median-in-a-set-of-27-floating-point-values/810905
                std::vector<double>::iterator first = value_list.begin();
                std::vector<double>::iterator last = value_list.end();
                std::vector<double>::iterator middle = first + (last - first) / 2;
                std::nth_element(first, middle, last);
                double median = *middle;
                //std::sort(value_list.begin(), value_list.end());
                //double median = value_list[value_list.size() / 2];
                guarded_plot(x, y, median);
            } else {
                guarded_plot(x, y, no_data_colour);
            }
        }
    }
}

void draw_datums_as_median_rolling(const DataSet& data_set, const Tile& tile) {
    double search_radius_in_meters = data_set.get_param_double("search_radius_in_meters");
    int minimum_points = data_set.get_param_int("minimum_points");
    if (minimum_points < 1)
        minimum_points = 1;
    double pixel_radius = tile.meters_to_pixels(search_radius_in_meters);
    int int_pixel_radius = int(pixel_radius) + 1;
    debug_log(boost::format("draw_datums_as_median_rolling: search_radius_in_meters %lf pixel_radius %lf") % search_radius_in_meters % pixel_radius);

    double pixel_radius_sq = pixel_radius * pixel_radius;

    DatumIndexList datum_index_list;
    std::vector<DatumIndexList> enters;
    std::vector<DatumIndexList> exits;
    enters.resize(IMAGE_WIDTH);
    exits.resize(IMAGE_WIDTH);
    for (int y = 0; y < IMAGE_HEIGHT; y++) {
        // Work out which datums might matter - in rectangle along whole row
        datum_index_list.clear();
        double x_1, y_1;
        tile.transform_tile_onto_merc(0 - int_pixel_radius, y - int_pixel_radius, x_1, y_1);
        double x_2, y_2;
        tile.transform_tile_onto_merc(IMAGE_WIDTH + int_pixel_radius, y + int_pixel_radius, x_2, y_2);
        datum_box_set_find_by_rectangle(data_set, x_1, y_1, x_2, y_2, datum_index_list);

        debug_log(boost::format("draw_datums_as_median_rolling: y %d datum count %d datums nearby %d") % y % data_set.entries.size() % datum_index_list.size());

        // Work out x-coordinates at which datums enter or leave the circle 
        for (int x = 0; x < IMAGE_WIDTH; x++) {
            enters[x].clear();
            exits[x].clear();
        }
        for (DatumIndexList::const_iterator it = datum_index_list.begin(); it != datum_index_list.end(); it++) {
            DatumIndex ix = *it;
            const Datum& datum = data_set.entries[ix];
            int datum_on_tile_x, datum_on_tile_y;
            tile.transform_merc_onto_tile(datum.x, datum.y, datum_on_tile_x, datum_on_tile_y);

            if (abs(datum_on_tile_y - y) <= int_pixel_radius) {
                int delta = calc_dist_fast_int_sub(int_pixel_radius, datum_on_tile_y - y);
                int enter_x = datum_on_tile_x - delta;
                int exit_x = datum_on_tile_x + delta;

                if (enter_x >= IMAGE_WIDTH && exit_x >= IMAGE_WIDTH)
                    continue;
                if (enter_x < 0 && exit_x < 0)
                    continue;
                if (enter_x < 0)
                    enter_x = 0;
                if (exit_x >= IMAGE_WIDTH - 1)
                    exit_x = IMAGE_WIDTH - 1;

                //debug_log(boost::format("draw_datums_as_median_rolling: datum on tile x %d y %d enter %d exit %d") % datum_on_tile_x % datum_on_tile_y % enter_x % exit_x);

                assert(enter_x <= IMAGE_WIDTH);
                assert(exit_x >= 0);

                enters[enter_x].push_back(ix);
                exits[exit_x].push_back(ix);
            }
        }

        // loop through X coordinates, inserting and removing datums as we come to them
        std::set<DatumIndex> datums;
        std::vector<double> value_list;
        for (int x = 0; x < IMAGE_WIDTH; x++) {
            // insert new points that sweep in
            BOOST_FOREACH(const DatumIndex& ix, enters[x]) {
                datums.insert(ix);
            }

            // work out values and median
            value_list.clear();
            BOOST_FOREACH(const DatumIndex& ix, datums) {
                const Datum& datum = data_set.entries[ix];
                value_list.push_back(datum.value);
            }

            if ((int)value_list.size() >= minimum_points) {
                // For discussion of quickly finding medians in C++ see
                // http://stackoverflow.com/questions/810657/fastest-code-c-c-to-select-the-median-in-a-set-of-27-floating-point-values/810905
                std::vector<double>::iterator first = value_list.begin();
                std::vector<double>::iterator last = value_list.end();
                std::vector<double>::iterator middle = first + (last - first) / 2;
                std::nth_element(first, middle, last);
                double median = *middle;
                //std::sort(value_list.begin(), value_list.end());
                //double median = value_list[value_list.size() / 2];
                guarded_plot(x, y, median);
            } else {
                guarded_plot(x, y, no_data_colour);
            }
             
            // remove points that are sweeping out
            BOOST_FOREACH(const DatumIndex& ix, exits[x]) {
                datums.erase(ix);
            }
        }
    }
}


/////////////////////////////////////////////////////////////////////
// Drawing functions - general

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


// render on tile according to parameters
void draw_on_tile(const DataSet& data_set, const Tile& tile) {
    int white = gdImageColorAllocate(im, 255, 255, 255);  
    gdImageFilledRectangle(im, 0, 0, IMAGE_WIDTH, IMAGE_HEIGHT, white);

    std::string algorithm = data_set.get_param("algorithm");
    std::string sub_algorithm = data_set.get_param("sub_algorithm");
    if (algorithm == "cones") {
        if (sub_algorithm == "by_datum") {
            draw_datums_as_cones_loop_by_datum(data_set, tile);
        } else if (sub_algorithm == "by_pixel") {
            draw_datums_as_cones_loop_by_pixel(data_set, tile);
        } else if (sub_algorithm == "drop_line") {
            draw_datums_as_cones_with_drop_line(data_set, tile);
        } else {
            assert(0);
        }
    } else if (algorithm == "median") {
        if (sub_algorithm == "naive") {
            draw_datums_as_median_naive(data_set, tile);
        } else if (sub_algorithm == "rolling") {
            draw_datums_as_median_rolling(data_set, tile);
        } else {
            assert(0);
        }
    } else if (algorithm == "test") {
        draw_pretty_test_pattern();
    } else {
        assert(0);
    }
    debug_log(boost::format("Plot count: %d Squareroot count: %d") % plot_count % sqrt_count);
}

// Draw a bunch of tiles at various zooms to benchmark things
void render_benchmark_tiles(const DataSet& data_set) {
    int tile_count = 0;
    int start_x = 1011 * 2;
    int start_y = 671 * 2;
    for (int z = 12; z > 5; --z) {
        for (int i = -2; i < 3; ++i) {
            for (int j = -2; j < 3; ++j) {
                // Work out which tile to go for 
                // XXX these tile_ would come from the URL e.g. iso/11/1011/671.png

                int zoom = z;
                int tile_x = start_x + i;
                int tile_y = start_y + j;

                Tile tile(zoom, tile_x, tile_y); // zoom, x, y as in URL, e.g. iso/11/1011/671.png
                debug_log(tile.debug_info());

                // Set pixel values
                PerformanceMonitor inner_pm;
                draw_on_tile(data_set, tile);
                tile_count++;
                inner_pm.display((boost::format("Plotting tile %d %d %d took") % zoom % tile_x % tile_y).str());
            }
        }
        start_x /= 2;
        start_y /= 2;
    }
    debug_log((boost::format("Image count: %d") % tile_count).str());
}

// Write out PNG file
void write_out_png(const Tile& tile, const std::string& filename) {
    FILE *out = fopen(filename.c_str(), "wb");
    gdImagePngEx(im, out, -1); // -1 is default compression, 0 is no compression
    fclose(out);
}

/////////////////////////////////////////////////////////////////////
// Main entry point

int main(int argc, char * argv[]) {
    PerformanceMonitor pm;
    DataSet data_set;

    if (argc != 2) {
        return 1;
    }

    std::string command;
    if (argc == 2) {
        command = argv[1];
    }
    if (command != "one" && command != "benchmark" && command != "fcgi" && command != "custom") {
        printf("drawtile.cpp: only argument must be command 'one', 'benchmark', 'fcgi' or 'custom'\n");
        return 1;
    }

    if (command == "custom") {
        double mercx, mercy;
        lat_lon_to_merc(53.466667, -2.233333, &mercx, &mercy); // Manchester
        printf("Manchester mercx, mercy: %lf %lf\n", mercx, mercy); // roughly: -248128.680454, 7071667.54412 (that's actually Manchester Picadilly)
        double lat, lon;
        merc_to_lat_lon(-248613.492332, 7069789.545191, &lat, &lon); // Manchester
        printf("Manchester lat, lon: %lf %lf\n", lat, lon); // 53.466667, -2.233333
        /*
        Tile t(11, 1011, 671); // zoom, x, y as in URL, e.g. iso/11/1011/671.png
        double merc_x, merc_y;
        t.transform_tile_onto_merc(IMAGE_WIDTH/2, IMAGE_HEIGHT/2, merc_x, merc_y);
        int google_url_x, google_url_y;
        int zoom = 8;
        Tile::merc_to_google_url(merc_x, merc_y, zoom, google_url_x, google_url_y);
        printf("Old: 11/1011/671 New google URL: %d/%d/%d\n", zoom, google_url_x, google_url_y);
        */
        return 0;
    }

    // Data to load
    std::string nodes_file = "/home/francis/toobig/nptdr/tmpwork/stations.nodes";
    std::string iso_file = "/home/francis/toobig/nptdr/tmpwork/1440.iso";
    // Algorithm to use
    data_set.params["algorithm"] = "cones";
    data_set.params["sub_algorithm"] = "by_datum";
    //data_set.params["sub_algorithm"] = "drop_line";
    data_set.params["max_walk_distance_in_meters"] = "2400"; // 2400 meters is a half hour of walking at 1.33333 m/s
    data_set.params["max_walk_time"] = "1800"; // 1800 seconds is half an hour 

    data_set.params["algorithm"] = "median";
    data_set.params["sub_algorithm"] = "rolling";
    data_set.params["search_radius_in_meters"] = "1000"; 
    data_set.params["minimum_points"] = "0"; 

    // Precalculate some things for optimisation
    calc_dist_fast_int_initialise();
    pm.display("Precalculating square roots took");

    // Read data set from .nodes file
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

    pm.display("Initialising data set took");
    datum_box_set_make(data_set, 1000); // XXX 1000 is just a guess an boxset optimisation parameter
    pm.display("Making box set took");
    debug_log(data_set.debug_info());

    // Create gd image surface
    im = gdImageCreateTrueColor(IMAGE_WIDTH, IMAGE_HEIGHT);
    pm.display("Creating surface took");
   
    // Display
    if (command == "benchmark") {
        render_benchmark_tiles(data_set); 
        pm.display("Total render time");
    } else if (command == "one") {
        Tile tile(11, 1011, 671);
        draw_on_tile(data_set, tile);
        pm.display("Tile render time");
        std::string outfile = "/tmp/drawtile.png";
        write_out_png(tile, outfile);
        pm.display("Writing PNG to " + outfile + " took");
    } else if (command == "fcgi") {
        //FCGX_IsCGI
        FCGX_Request request;
        FCGX_Stream *in, *out, *err;
        FCGX_ParamArray envp;
        if (FCGX_InitRequest(&request, 0, 0) != 0)
            throw Exception("FCGX_InitRequest failed");
        while (FCGX_Accept(&in, &out, &err, &envp) == 0) {
            std::string bytes;
            // Parse the parameters
            std::string path_info = FCGX_GetParam("PATH_INFO", envp);
            std::vector<std::string> parts;
            std::string sofar;
            for (unsigned int i = 0; i < path_info.size(); ++i) {
                char c = path_info[i];
                if (c == '/') {
                    parts.push_back(sofar);
                    sofar = "";
                } else {
                    sofar += c;
                }
            }
            parts.push_back(sofar);
            if (parts.size() == 5) {
                // Convert parameters from strings to integers
                std::string layer;
                int x, y, z;
                layer = parts[1];
                x = atoi(parts[2].c_str());
                y = atoi(parts[3].c_str());
                z = atoi(parts[4].c_str());

                // Render the tile and return as a PNG
                Tile tile(x, y, z);
                draw_on_tile(data_set, tile);
                int size;
                void *png_ptr = gdImagePngPtr(im, &size);
                int ret = FCGX_PutS("Content-type: image/png\n\n", out);
                ret = FCGX_PutStr((char *)png_ptr, size, out);
                gdFree(png_ptr);

                // Log success
                pm.display((boost::format("drawtile.cpp: Handled FCGI request for layer %s tile %d/%d/%d in") % layer % z % x % y).str());
            } else {
                // User error
                bytes = (boost::format("Content-type: text/html\n\nFailed to parse PATH_INFO as /layer/zoom/x/y")).str();
                int ret = FCGX_PutS(bytes.c_str(), out);
            }
            FCGX_Finish();
        }
    } else {
        assert(0);
    }
}


