#
# fastplan.py:
# Ouputs data structure for use making plans, as makeplan.py, but from a faster
# separate C++ programme.
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: francis@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: fastplan.py,v 1.12 2009-03-26 09:39:28 francis Exp $
#

import logging
import datetime
import sys
import os
import math
import struct

sys.path.append(sys.path[0] + "/../../pylib") # XXX this is for running doctests and is nasty, there's got to be a better way
import mysociety.atcocif
      
class FastPregenATCO(mysociety.atcocif.ATCO):
    def __init__(self, out_prefix, nptdr_files, target_date, show_progress = False):
        self.out_prefix = out_prefix
        self.nptdr_files = nptdr_files
        self.target_date = target_date
        self.show_progress = show_progress

    def run_pregen(self):
        # output locations in binary
        logging.info("FastPregenATCO: making locations file")
        self.file_locations = open(self.out_prefix + ".locations", 'w')
        # ... make space for count which we will only know at the end ...
        self._pack(self.file_locations, "=i", -1) 
        # ... output locations, counting and giving them ids as we go 
        self.location_c = 0
        self.location_to_fastix = {}
        self.read_all(self.load_locations)
        # ... fill in count now we know it
        self.file_locations.seek(0)
        self._pack(self.file_locations, "=i", len(self.location_to_fastix))
        # ... close file
        self.file_locations.close()

        # output journeys in binary
        logging.info("FastPregenATCO: making journey file")
        self.file_journeys = open(self.out_prefix + ".journeys", 'w')
        # make space for count which we will only know at the end ...
        self._pack(self.file_journeys, "=i", -1) 
        # ... output journeys, counting and giving them ids as we go 
        self.journey_c = 0
        self.journey_to_fastix = {}
        self.read_all(self.load_journeys)
        # ... fill in count now we know it
        self.file_journeys.seek(0)
        self._pack(self.file_journeys, "=i", len(self.journey_to_fastix))
        # ... close file
        self.file_journeys.close()

    # reload all ATCO files, setting load function to given one
    def read_all(self, func):
        # change the loading function to the one asked for
        self.item_loaded = func
        # do the loading
        self.read_files(self.nptdr_files)

    # Pass output all locations
    def load_locations(self, item):
        # locations only
        if not isinstance(item, mysociety.atcocif.Location):
            return

        # see if we already got this one
        if item.location in self.location_to_fastix:
            return

        # we count here, so the ids don't change if we do find a grid reference
        # for stations which miss one later
        self.location_c += 1

        # if it has no grid reference, give up on it
        if item.additional.grid_reference_easting <= 0 or item.additional.grid_reference_northing <= 0:
            logging.warn("location %s doesn't have grid coordinates, dropping it" % (item.location))
            return

        # output it
        self.location_to_fastix[item.location] = self.location_c
        self._pack(self.file_locations, "=ih%dsii" % len(item.location), self.location_c, len(item.location), item.location, item.additional.grid_reference_easting, item.additional.grid_reference_northing)

    # Pass to output all journeys
    def load_journeys(self, item):
        # journeys only
        if not isinstance(item, mysociety.atcocif.JourneyHeader):
            return

        # ditch journeys which aren't valid on the date
        if not item.is_valid_on_date(self.target_date):
            return
        # ditch journeys which don't have location information
        bad = False
        for hop in item.hops:
            if hop.location not in self.location_to_fastix:
                logging.warn("location %s appears in journey %s but isn't in locations list" % (hop.location, item.id))
                bad = True
        if bad:
            return
        # see if we already got this one
        if item.id in self.journey_to_fastix:
            return

        # output it
        self.journey_c += 1
        self.journey_to_fastix[item.id] = self.journey_c
        vehicle_type = 'B'
        if item.vehicle_type == 'TRAIN':
            vehicle_type = 'T'
        self._pack(self.file_journeys, "=ih%dsch" % len(item.id), self.journey_c, len(item.id), item.id, vehicle_type, len(item.hops))
        for hop in item.hops:
            mins_arr,mins_dep = -1,-1
            if hop.is_set_down():
                mins_arr = hop.published_arrival_time.hour * 60 + hop.published_arrival_time.minute
            if hop.is_pick_up():
                mins_dep = hop.published_departure_time.hour * 60 + hop.published_departure_time.minute
            self._pack(self.file_journeys, "=ihh", self.location_to_fastix[hop.location], mins_arr, mins_dep)


    # Internal binary packing function, with logging for debugging
    def _pack(self, handle, *args):
        binout = struct.pack(*args)
        logging.debug("packing: " + repr(args) + " => " + repr(binout))
        handle.write(binout)



if __name__ == "__main__":
    import doctest
    doctest.testmod()

