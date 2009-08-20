//
// drawtile.cpp:
//
// Renders a contour tile.
//
// Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
// Email: francis@mysociety.org; WWW: http://www.mysociety.org/
//
// $Id: drawtile.cpp,v 1.1 2009-08-20 16:54:12 francis Exp $
//

#include <math.h> 
#include <gd.h>
#include <vector>

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
typedef std::vector<Datum> DatumList;
float datum_radius = 25;


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
void draw_datums_as_cones_loop_by_datum(const DatumList& datum_list) {
    //gdImageFilledRectangle(im, 0, 0, image_width - 1, image_height - 1, no_data_colour); 
    //gdImageFilledRectangle(im, 0, 0, 100, 100, 10000); 
    //return;

    for (DatumList::const_iterator it = datum_list.begin(); it != datum_list.end(); it++) {
        const Datum& datum = *it;
        for (int x = -datum_radius; x <= datum_radius ; x++) {
            for (int y = -datum_radius; y <= datum_radius; y++) {
                int plot_x = datum.x + x;
                int plot_y = datum.y + y;
                double dist = sqrt(x * x + y * y);
                if (dist <= datum_radius) {
                    guarded_min_plot(plot_x, plot_y, dist * test_multiple_factor + datum.value);
                }
            }
        }

    }
}

// Efficient version of draw_datums_as_cones_loop_by_datum, which loops over pixels
// rather than over cones.
void draw_datums_as_cones_loop_by_pixel(const DatumList& datum_list) {
    for (int x = 0; x < image_width ; x++) {
        for (int y = 0; y < image_height; y++) {
            // XXX should magically find nearby datums rather than loop over all of them
            double min_dist = -1;
            double min_value = -1;
            for (DatumList::const_iterator it = datum_list.begin(); it != datum_list.end(); it++) {
                const Datum& datum = *it;

                int rel_x = datum.x - x;
                int rel_y = datum.y - y;

                if (rel_x < -datum_radius || rel_x > datum_radius || rel_y < -datum_radius  || rel_y > datum_radius) {
                    continue;
                }

                double dist = sqrt(rel_x * rel_x + rel_y * rel_y);
                if (dist <= datum_radius && (min_dist == -1 || dist * test_multiple_factor + datum.value < min_dist * test_multiple_factor + min_value)) {
                    min_dist = dist;
                    min_value = datum.value;
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
    /*if (argc < 7) {
        fprintf(stderr, "fastplan.cpp arguments are:\n  1. fast index file prefix\n  2. output prefix (or 'stream' for stdout incremental)\n  3. arrive_by or depart_after\n  4. target arrival time / departure in mins after midnight\n  5. target location\n  6. earliest/latest departure in mins after midnight to go back to\n  7, 8. easting, northing to use to find destination if destination is 'coordinate'\n");
        return 1;
    }*/

    DatumList datum_list;
    int c = 0;
    for (int i = 3; i < 20; i++) {
        for (int j = 3; j < 20; j++) {
            c++;
            datum_list.push_back(Datum(i * 12, j * 12, c * 5));
        }
    }
    log(boost::format("Number of datums: %d") % datum_list.size());

    // Create gd image surface
    im = gdImageCreateTrueColor(image_width, image_height);

    // Set pixel values
    //draw_pretty_test_pattern();
    //draw_datums_as_cones_loop_by_datum(datum_list);
    draw_datums_as_cones_loop_by_pixel(datum_list);

    // Write out PNG file
    FILE *out = fopen ("/tmp/drawtile.png", "wb");
    gdImagePngEx(im, out, -1); // -1 is default compression, 0 is no compression
    fclose(out);
}


