//
// drawtile.cpp:
//
// Renders a contour tile.
//
// Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
// Email: francis@mysociety.org; WWW: http://www.mysociety.org/
//
// $Id: drawtile.cpp,v 1.2 2009-08-21 01:26:21 francis Exp $
//

#include <math.h> 
#include <gd.h>
#include <assert.h>

#include <vector>
#include <list>

#include "../../cpplib/mysociety_error.h"
#include "../cpplib/performance_monitor.h"

/* Any size of tile you like, as long as it is 256x256 pixels */
int image_width = 256;
int image_height = 256;
gdImagePtr im;
//double sqrt_cache[image_width][image_height];

int no_data_colour = -1;

/* Plot a pixel on a tile, check values in range */
void guarded_plot(int x, int y, int col) {
    if (x >= 0 && y >= 0 && x < image_width && y < image_height) {
        //log(boost::format("plotting: %d %d colour: %d") % x % y % col);
        gdImageTrueColorPixel(im, x, y) = col;
    }
}

/* Plot a pixel on a tile, check values in range, but use the minimum value */
void guarded_min_plot(int x, int y, int col) {
    if (x >= 0 && y >= 0 && x < image_width && y < image_height) {
        int current_col = gdImageTrueColorPixel(im, x, y);
        if (current_col == 0 || col < current_col) {
            gdImageTrueColorPixel(im, x, y) = col;
        }
    }
}

// A datum stores an item of the input data set. Has a coordinate, and data
// value. The data value will, for example, be journey time, house price, wind
// speed.
class Datum {
    public:
    double x;
    double y;
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

    // ranges allowed for datum locations
    double x_min, x_max; 
    double y_min, y_max;

    // maximum distance away from a datum that it can affect contour tile colour.
    // also used as cone radius for minimum cone algorithm.
    double effect_radius;

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

// For drawing cones, scale the height of the cone by this much
int test_multiple_factor = 10;

// Draw some inverted cones on the tile. The cones are inverted, with their point
// at the bottom. The height of the point is the value of the datum, its centre
// point is the position of the datum. The height is used as the colour value of
// the pixel. When two cones are drawn on top of each other, the minimum height
// is used. This algorithm is, for example, used for making contours of travel
// time by public transport.
void draw_datums_as_cones_loop_by_datum(const DataSet& data_set) {
    //gdImageFilledRectangle(im, 0, 0, image_width - 1, image_height - 1, no_data_colour); 
    //gdImageFilledRectangle(im, 0, 0, 100, 100, 10000); 
    //return;

    for (DatumEntries::const_iterator it = data_set.entries.begin(); it != data_set.entries.end(); it++) {
        const Datum& datum = *it;
        for (int x = -data_set.effect_radius; x <= data_set.effect_radius ; x++) {
            for (int y = -data_set.effect_radius; y <= data_set.effect_radius; y++) {
                int plot_x = datum.x + x;
                int plot_y = datum.y + y;
                double dist = sqrt(x * x + y * y);
                if (dist <= data_set.effect_radius) {
                    guarded_min_plot(plot_x, plot_y, dist * test_multiple_factor + datum.value);
                }
            }
        }

    }
}

// Efficient version of draw_datums_as_cones_loop_by_datum, which loops over pixels
// rather than over cones.
void draw_datums_as_cones_loop_by_pixel(const DataSet& data_set) {
    for (int x = 0; x < image_width ; x++) {
        for (int y = 0; y < image_height; y++) {
            // XXX should magically find nearby datums rather than loop over all of them
            double min_dist = -1;
            double min_value = -1;

            int center_box_x, center_box_y;
            box_set_square_at_point(data_set, x, y, center_box_x, center_box_y); // XXX convert x and y
            int box_range_min_x = (center_box_x > 0) ? (center_box_x - 1) : center_box_x;
            int box_range_max_x = (center_box_x < data_set.box_set_width - 1) ? (center_box_x + 1) : center_box_x;
            int box_range_min_y = (center_box_y > 0) ? (center_box_y - 1) : center_box_y;
            int box_range_max_y = (center_box_y < data_set.box_set_height - 1) ? (center_box_y + 1) : center_box_y;
            for (int box_y = box_range_min_y; box_y <=  box_range_max_y; box_y++) {
                for (int box_x = box_range_min_x; box_x <=  box_range_max_x; box_x++) {
                    const DatumIndexList& datum_index_list = data_set.box_set[box_x][box_y];
                    for (DatumIndexList::const_iterator it = datum_index_list.begin(); it != datum_index_list.end(); it++) {
                        DatumIndex ix = *it;
                        const Datum& datum = data_set.entries[ix];

                        int rel_x = datum.x - x;
                        int rel_y = datum.y - y;

                        if (rel_x < -data_set.effect_radius || rel_x > data_set.effect_radius || rel_y < -data_set.effect_radius  || rel_y > data_set.effect_radius) {
                            continue;
                        }

                        double dist = sqrt(rel_x * rel_x + rel_y * rel_y);
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

int main(int argc, char * argv[]) {
    PerformanceMonitor pm;

    /*if (argc < 7) {
        fprintf(stderr, "fastplan.cpp arguments are:\n  1. fast index file prefix\n  2. output prefix (or 'stream' for stdout incremental)\n  3. arrive_by or depart_after\n  4. target arrival time / departure in mins after midnight\n  5. target location\n  6. earliest/latest departure in mins after midnight to go back to\n  7, 8. easting, northing to use to find destination if destination is 'coordinate'\n");
        return 1;
    }*/

    DataSet data_set;
    data_set.x_min = 0.0;
    data_set.x_max = 255.0;
    data_set.y_min = 0.0;
    data_set.y_max = 255.0;
    data_set.effect_radius = 25.0;
    int c = 0;
    for (int i = 3; i < 20; i++) {
        for (int j = 3; j < 20; j++) {
            c++;
            data_set.entries.push_back(Datum(i * 12, j * 12, c * 5));
        }
    }
    pm.display("Initialising data set took");
    make_datum_box_set(data_set);
    log(boost::format("Number of datums: %d") % data_set.entries.size());
    pm.display("Making box set took");

    // Create gd image surface
    im = gdImageCreateTrueColor(image_width, image_height);
    pm.display("Creating surface took");

    // Set pixel values
    //draw_pretty_test_pattern();
    //draw_datums_as_cones_loop_by_datum(data_set);
    draw_datums_as_cones_loop_by_pixel(data_set);
    pm.display("Plotting image took");

    // Write out PNG file
    FILE *out = fopen ("/tmp/drawtile.png", "wb");
    gdImagePngEx(im, out, -1); // -1 is default compression, 0 is no compression
    fclose(out);
    pm.display("Writing PNG took");
}


