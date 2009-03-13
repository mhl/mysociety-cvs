#
# fastplan.py:
# Ouputs data structure for use making plans, as makeplan.py, but from a faster
# separate C++ programme.
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: francis@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: fastplan.py,v 1.10 2009-03-13 11:23:45 francis Exp $
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
        # count stuff
        logging.info("FastPregenATCO: counting things")
        self.location_c = 0
        self.location_to_fastix = {}
        self.journey_c = 0
        self.journey_to_fastix = {}
        self.read_all(self.count_stuff)
        
        # output location ids
        logging.info("FastPregenATCO: making locations file")
        self.file_locations = open(self.out_prefix+".locations", 'w')
        self._pack(self.file_locations, "=i", len(self.location_to_fastix))
        self.location_c = 0
        self.location_to_fastix = {}
        self.read_all(self.load_locations)
        self.file_locations.close()

        # output journey ids
        logging.info("FastPregenATCO: making journey file")
        self.file_journeys = open(self.out_prefix+".journeys", 'w')
        self._pack(self.file_journeys, "=i", len(self.journey_to_fastix))
        self.journey_c = 0
        self.journey_to_fastix = {}
        self.read_all(self.load_journeys)
        self.file_journeys.close()

    # reload all ATCO files, setting load function to given one
    def read_all(self, func):
        # change the loading function to the one asked for
        self.item_loaded = func
        # do the loading
        self.read_files(self.nptdr_files)

    # Pass to count things
    def count_stuff(self, item):
        if isinstance(item, mysociety.atcocif.Location):
            if item.location not in self.location_to_fastix:
                self.location_c += 1
                self.location_to_fastix[item.location] = self.location_c
        elif isinstance(item, mysociety.atcocif.JourneyHeader):
            # ditch journeys which aren't valid on the date
            if not item.is_valid_on_date(self.target_date):
                return
            if item.id not in self.journey_to_fastix:
                self.journey_c += 1
                self.journey_to_fastix[item.id] = self.journey_c
    
    # Pass output all locations
    def load_locations(self, item):
        if isinstance(item, mysociety.atcocif.Location):
            if item.location not in self.location_to_fastix:
                self.location_c += 1
                self.location_to_fastix[item.location] = self.location_c
                assert item.additional.grid_reference_easting > 0, "missing coordinate, easting is: " + str(item.additional.grid_reference_easting)
                assert item.additional.grid_reference_northing > 0, "missing coordinate, northing is: " + str(item.additional.grid_reference_northing)
                self._pack(self.file_locations, "=ih%dsii" % len(item.location), self.location_c, len(item.location), item.location, item.additional.grid_reference_easting, item.additional.grid_reference_northing)

    # Pass to output all journeys
    def load_journeys(self, item):
        if isinstance(item, mysociety.atcocif.JourneyHeader):
            # ditch journeys which aren't valid on the date
            if not item.is_valid_on_date(self.target_date):
                return
            # if this is a new one, then use it
            if item.id not in self.journey_to_fastix:
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

