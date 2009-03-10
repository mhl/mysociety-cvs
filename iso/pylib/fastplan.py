#
# fastplan.py:
# Ouputs data structure for use making plans, as makeplan.py, but from a faster
# separate C++ programme.
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: francis@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: fastplan.py,v 1.2 2009-03-10 17:27:40 francis Exp $
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
    def __init__(self, out_prefix, nptdr_files, target_date):
        self.out_prefix = out_prefix
        self.nptdr_files = nptdr_files
        self.target_date = target_date

        # count stuff
        self.number_of_locations = 0
        self.number_of_journeys = 0
        self.read_all(self.count_stuff)

        # output location ids
        self.file_locations = open(self.out_prefix+".locations", 'w')
        self._pack(self.file_locations, "i", self.number_of_locations)
        self.location_c = 0
        self.location_to_fastix = {}
        self.read_all(self.load_location_ids)

        # output journey ids
        self.file_journeys = open(self.out_prefix+".journeys", 'w')
        self._pack(self.file_journeys, "i", self.number_of_journeys)
        self.journey_c = 0
        self.journey_to_fastix = {}
        self.read_all(self.load_journey_ids)

    # reload all ATCO files, setting load function to given one
    def read_all(self, func):
        # change the loading function to the one asked for
        self.item_loaded = func
        # do the loading
        for nptdr_file in self.nptdr_files:
            self.read(nptdr_file)

    # Pass to count things
    def count_stuff(self, item):
        if isinstance(item, mysociety.atcocif.Location):
            self.number_of_locations += 1
        if isinstance(item, mysociety.atcocif.JourneyHeader):
            self.number_of_journeys += 1
    
    # Pass to give numeric identifier to all locations.
    def load_location_ids(self, item):
        if isinstance(item, mysociety.atcocif.Location):
            if item.location not in self.location_to_fastix:
                self.location_c += 1
                self.location_to_fastix[item.location] = self.location_c
                self._pack(self.file_locations, "ipii", self.location_c, item.location, item.additional.grid_reference_easting, item.additional.grid_reference_northing)

    # Pass to give numeric identifier to all journeys
    def load_journey_ids(self, item):
        if isinstance(item, mysociety.atcocif.JourneyHeader):
            # ditch journeys which aren't valid on the date
            if not item.is_valid_on_date(self.target_date):
                return
            # if this is a new one, then use it
            if item.id not in self.journey_to_fastix:
                self.journey_c += 1
                self.journey_to_fastix[item.id] = self.journey_c
                self._pack(self.file_journeys, "ip", self.journey_c, item.id)
                for hop in item.hops:
                    mins_arr,mins_dep = -1,-1
                    if hop.is_set_down():
                        mins_arr = hop.published_arrival_time.hour * 60 + hop.published_arrival_time.second
                    if hop.is_pick_up():
                        mins_dep = hop.published_departure_time.hour * 60 + hop.published_departure_time.second
                    self._pack(self.file_locations, "ihh", self.location_to_fastix[hop.location], mins_arr, mins_dep)



    # Internal binary packing function, with logging for debugging
    def _pack(self, handle, *args):
        logging.debug("packing: " + repr(args))
        binout = struct.pack(*args)
        handle.write(binout)



if __name__ == "__main__":
    import doctest
    doctest.testmod()

