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
// $Id: drawtile.cpp,v 1.7 2009-09-24 23:24:07 francis Exp $
//

// TODO:
// Coordinate transforms (how do effect_radius?)
// Box set size should surely be effect_radius * 2 not just effect_radius
// Move im to be member of Tile?
// Cache pixels_per_meter
// Sort out great circle distance difference (pixel radius)
// Put back time to 1800 seconds like it should be 

#include <math.h> 
#include <gd.h>
#include <assert.h>
#include <float.h>

#include <sys/types.h>
#include <sys/stat.h>

#include <vector>
#include <list>
#include <map>

#include "../../cpplib/mysociety_error.h"
#include "../../cpplib/mysociety_geo.h"
#include "../cpplib/performance_monitor.h"

/* Any size of tile you like, as long as it is 256x256 pixels */
int image_width = 256;
int image_height = 256;
double image_diagonal = sqrt(image_width * image_width + image_height * image_height);
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
//double sqrt_cache[image_width][image_height];
double calc_dist(double x, double y) {
    sqrt_count++;
    return sqrt(x * x + y * y);
}

/* Plot a pixel on a tile, check values in range.
   Note: GD has Y going down the page, in spherical mercator coords it goes up.
   That's why we flip the Y value just before drawing.
*/
void guarded_plot(int x, int y, int col) {
    plot_count++;
    if (x >= 0 && y >= 0 && x < image_width && y < image_height) {
        //debug_log(boost::format("plotting: %d %d colour: %d") % x % y % col);
        gdImageTrueColorPixel(im, x, image_height - 1 - y) = col; 
    }
}

/* Plot a pixel on a tile, check values in range, but use the minimum value */
void guarded_min_plot(int x, int y, int col) {
    if (x >= 0 && y >= 0 && x < image_width && y < image_height) {
        int current_col = gdImageTrueColorPixel(im, x, image_height - 1 - y);
        if (current_col == 0 || col < current_col) {
            gdImageTrueColorPixel(im, x, image_height - 1 - y) = col;
        }
    }
    plot_count++;
}

/////////////////////////////////////////////////////////////////////
// Tiles - transforming between mercator position and tile URL/zoom

class Tile {
    public:
    Tile(int l_zoom, int l_google_url_x, int l_google_url_y) {
        this->zoom = l_zoom;

        double res = merc_max_resolution / double(1 << this->zoom);
        //self.resolutions = [maxRes / 2 ** i for i in range(zoom_levels))]
        //res  = self.layer.resolutions[self.z]

        this->x = l_google_url_x;
        // flip Y value - the URLs we use are Google URLs (tms_type='google' in
        // the terminology of tilecache), but internally we use the Tile Map
        // Service Specification
        // (http://wiki.osgeo.org/wiki/Tile_Map_Service_Specification)
        // convention. i.e. Y increases as you head North.
        int max_url_y = int(round( (merc_y_orig_max - merc_y_orig_min) / (res * image_height))) - 1;
        this->y = max_url_y - l_google_url_y;

        this->min_x_merc = merc_x_orig_min + (res * this->x * image_width);
        this->min_y_merc = merc_y_orig_min + (res * this->y * image_height);
        this->max_x_merc = merc_x_orig_min + (res * (this->x + 1) * image_width);
        this->max_y_merc = merc_y_orig_min + (res * (this->y + 1) * image_height);
    }

    // Convert a mercator coordinate into a pixel coordinate on the tile
    // XXX could output doubles here for accuracy for other purposes
    void transform_merc_onto_tile(double merc_x, double merc_y, int& tile_x, int &tile_y) const {
        /*assert(merc_x >= this->min_x_merc);
        assert(merc_x <= this->max_x_merc);
        assert(merc_y >= this->min_y_merc);
        assert(merc_y <= this->max_y_merc);*/

        tile_x = (merc_x - min_x_merc) / (max_x_merc - min_x_merc) * image_width;
        tile_y = (merc_y - min_y_merc) / (max_y_merc - min_y_merc) * image_height;
    }

    std::string debug_info() {
        return (boost::format("Tile: zoom/x/y: %d/%d/%d merc-x-range: %lf %lf merc-y-range: %lf %lf pixels/m: %lf") % this->zoom % this->x % this->y % min_x_merc % max_x_merc % min_y_merc % max_y_merc % this->pixels_per_meter()).str();
    }

    // Number of pixels per meter of spherical globe in current projection.
    double pixels_per_meter() const {
        double lon1, lat1;
        double lon2, lat2;
        merc_to_lat_lon(this->min_x_merc, this->min_y_merc, &lat1, &lon1);
        merc_to_lat_lon(this->max_x_merc, this->max_y_merc, &lat2, &lon2);
        //debug_log(boost::format("pixels_per_meter: internal lat1 lon1 %lf %lf") % lat1 % lon1);
        //debug_log(boost::format("pixels_per_meter: internal lat2 lon2 %lf %lf") % lat2 % lon2);

        // XXX This great_circle_distance returns (a bit) different results to kilometers_between in tilecache
        double diagonal_1_in_m = great_circle_distance(lat1, lon1, lat2, lon2);
        double diagonal_2_in_m = great_circle_distance(lat1, lon2, lat2, lon1);
        double average_diagonal_in_m = (diagonal_1_in_m + diagonal_2_in_m) / 2;
        //debug_log(boost::format("pixels_per_meter: internal diagonal_1_in_m diagonal_2_in_m %lf %lf") % diagonal_1_in_m % diagonal_2_in_m);

        return image_diagonal / average_diagonal_in_m;
    }

    // Convert a distance in meters to an approximate distance in pixels on the tile
    double meters_to_pixels(double distance) const {
        double pixels = distance * this->pixels_per_meter();
        return pixels;
    }

    int zoom;
    int x, y;

    double min_x_merc, max_x_merc;
    double min_y_merc, max_y_merc;
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

    // maximum distance away from a datum that it can affect contour tile colour.
    // also used as cone radius for minimum cone algorithm.
    double effect_radius; // XXX deprecated

    // used to quickly find datum t
    int box_set_width, box_set_height;
    DatumBoxSet box_set;
};

// Create a grid of squares, each datum going into one squares. Squares are same size
// as the maximum radius that a datum can affect the tile colour.
void make_datum_box_set(DataSet& data_set) {
    DatumBoxSet& box_set = data_set.box_set;
    box_set.clear();

    // work out how many entries their in box set
    int box_set_width = (data_set.x_max - data_set.x_min) / data_set.effect_radius + 1;
    int box_set_height = (data_set.y_max - data_set.y_min) / data_set.effect_radius + 1;
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

        int box_x = (datum.x - data_set.x_min) / data_set.effect_radius;
        int box_y = (datum.y - data_set.y_min) / data_set.effect_radius;

        assert(box_x >= 0);
        assert(box_x < box_set_width);
        assert(box_y >= 0);
        assert(box_y < box_set_height);

        DatumIndexList &datum_index_list = box_set[box_x][box_y];
        datum_index_list.push_back(ix);
    }
}
// Given a point (a datum, essentially), return the position of the box set grid cell that contains that point.
void box_set_square_at_point(const DataSet& data_set, const double x, const double y, int& box_x, int& box_y) {
    box_x = (x - data_set.x_min) / data_set.effect_radius;
    box_y = (y - data_set.y_min) / data_set.effect_radius;
    // make sure it is in bounds
    if (box_x < 0) box_x = 0;
    if (box_x >= data_set.box_set_width) box_x = data_set.box_set_width - 1;
    if (box_y < 0) box_y = 0;
    if (box_y >= data_set.box_set_height) box_y = data_set.box_set_height - 1;
}

// Draw a test pattern on the tile
void draw_pretty_test_pattern() {
    int d = 0;
    for (int x = 0; x < image_width; x++) {
        for (int y = 0; y < image_height; y++) {
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
    debug_log(boost::format("pixel_radius: %lf") % pixel_radius);
    pixel_radius = 54.451374078082381; // XXX fix me :) is the great circle distance difference

    for (DatumEntries::const_iterator it = data_set.entries.begin(); it != data_set.entries.end(); it++) {
        const Datum& datum = *it;
        int datum_on_tile_x, datum_on_tile_y;
        tile.transform_merc_onto_tile(datum.x, datum.y, datum_on_tile_x, datum_on_tile_y);
        if (datum_on_tile_x > 0 && datum_on_tile_y > 0 && datum_on_tile_x < image_width && datum_on_tile_y < image_height) {
            debug_log(boost::format("datum merc: %lf %lf datum tile place: %d %d value: %d") % datum.x % datum.y % datum_on_tile_x % datum_on_tile_y %datum.value);
        }
        // guarded_min_plot(datum_on_tile_x, datum_on_tile_y, 1000000);
        //continue;
        for (int x = -pixel_radius; x <= pixel_radius; x++) {
            for (int y = -pixel_radius; y <= pixel_radius; y++) {
                int plot_x = datum_on_tile_x + x;
                int plot_y = datum_on_tile_y + y;
                double dist = calc_dist(x, y);
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
int test_multiple_factor = 1; // XXX deprecated
void draw_datums_as_cones_loop_by_pixel(const DataSet& data_set) {
    for (int x = 0; x < image_width ; x++) {
        for (int y = 0; y < image_height; y++) {
            //debug_log(boost::format("Plot place: %d %d") % x % y);

            // XXX should magically find nearby datums rather than loop over all of them
            double min_dist = -1;
            double min_value = -1;

            int center_box_x, center_box_y;
            box_set_square_at_point(data_set, x, y, center_box_x, center_box_y); // XXX convert x and y
            int box_range_min_x = (center_box_x > 0) ? (center_box_x - 1) : center_box_x;
            int box_range_max_x = (center_box_x < data_set.box_set_width - 1) ? (center_box_x + 1) : center_box_x;
            int box_range_min_y = (center_box_y > 0) ? (center_box_y - 1) : center_box_y;
            int box_range_max_y = (center_box_y < data_set.box_set_height - 1) ? (center_box_y + 1) : center_box_y;
            for (int box_x = box_range_min_x; box_x <= box_range_max_x; box_x++) {
                for (int box_y = box_range_min_y; box_y <= box_range_max_y; box_y++) {
                    const DatumIndexList& datum_index_list = data_set.box_set[box_x][box_y];
                    for (DatumIndexList::const_iterator it = datum_index_list.begin(); it != datum_index_list.end(); it++) {
                        DatumIndex ix = *it;
                        const Datum& datum = data_set.entries[ix];

                        int rel_x = datum.x - x;
                        int rel_y = datum.y - y;

                        if (rel_x < -data_set.effect_radius || rel_x > data_set.effect_radius || rel_y < -data_set.effect_radius  || rel_y > data_set.effect_radius) {
                            continue;
                        }

                        double dist = calc_dist(rel_x, rel_y);
                        if (dist <= data_set.effect_radius && (min_dist == -1 || dist * test_multiple_factor + datum.value < min_dist * test_multiple_factor + min_value)) {
                            min_dist = dist;
                            min_value = datum.value;
                        }
                    }
                }
            }

            if (min_dist != -1) {
                guarded_plot(x, y, min_dist * test_multiple_factor + min_value);
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

    double mercx, mercy;
    lat_lon_to_merc(53.466667, -2.233333, &mercx, &mercy); // Manchester
    printf("Manchester mercx, mercy: %lf %lf\n", mercx, mercy); // roughly: -248128.680454, 7071667.54412 (that's actually Manchester Picadilly)
    double lat, lon;
    merc_to_lat_lon(-248613.492332, 7069789.545191, &lat, &lon); // Manchester
    printf("Manchester lat, lon: %lf %lf\n", lat, lon); // 53.466667, -2.233333

    /*if (argc < 7) {
        fprintf(stderr, "fastplan.cpp arguments are:\n  1. fast index file prefix\n  2. output prefix (or 'stream' for stdout incremental)\n  3. arrive_by or depart_after\n  4. target arrival time / departure in mins after midnight\n  5. target location\n  6. earliest/latest departure in mins after midnight to go back to\n  7, 8. easting, northing to use to find destination if destination is 'coordinate'\n");
        return 1;
    }*/

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
    data_set.params["max_walk_time"] = 2400; // 1800 seconds is half an hour XXX change it back to that value

    // Internal test populate data set
    /*
    data_set.effect_radius = 10.0;
    int c = 0;
    for (int i = 3; i < 10; i++) {
        for (int j = 3; j < 10; j++) {
            c++;
            data_set.add_datum(i * 24, j * 24, c * 5);
        }
    }
    */

    pm.display("Initialising data set took");
    // make_datum_box_set(data_set);
    // pm.display("Making box set took");
    debug_log(data_set.debug_info());

    // Work out which tile to go for 
    // XXX these tile_ would come from the URL e.g. iso/11/1011/671.png
    Tile tile(11, 1011, 671); // zoom, x, y as in URL, e.g. iso/11/1011/671.png
    debug_log(tile.debug_info());

    // Create gd image surface
    im = gdImageCreateTrueColor(image_width, image_height);
    int white = gdImageColorAllocate(im, 255, 255, 255);  
    gdImageFilledRectangle(im, 0, 0, image_width, image_height, white);
    pm.display("Creating surface took");

    // Set pixel values
    //draw_pretty_test_pattern();
    draw_datums_as_cones_loop_by_datum(data_set, tile);
    //draw_datums_as_cones_loop_by_pixel(data_set);
    debug_log(boost::format("Plot count: %d Squareroot count: %d") % plot_count % sqrt_count);
    pm.display("Plotting image took");

    // Write out PNG file
    FILE *out = fopen ("/tmp/drawtile.png", "wb");
    gdImagePngEx(im, out, -1); // -1 is default compression, 0 is no compression
    fclose(out);
    pm.display("Writing PNG took");
}


