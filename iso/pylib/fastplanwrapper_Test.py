from __future__ import with_statement

import unittest

import os
import os.path

import sys
sys.path.append('../../pylib/')

import mysociety.config
mysociety.config.set_file('../conf/unittest')

import fastplanwrapper

# Needed so that the module imports and we can set this
# when __name__ == '__main__'
shared_fastplan_pipe = None

# Location for storing the output files
TMP_DIR = mysociety.config.get('TMPWORK')

class TestFastPlan(unittest.TestCase):
    def test_fastplan(self):
        """Send a test case to fastplan and check it comes back."""

        outfile = os.path.join(TMP_DIR, 'test_out')
        outfile_routes = os.path.join(TMP_DIR, 'test_out_routes')

        results = fastplanwrapper.fastplan(shared_fastplan_pipe, 
                                           outfile, 
                                           outfile_routes,
                                           'arrive_by', 
                                           540, 
                                           0, 
                                           '', 
                                           393451, 
                                           804639)
        print results

        # FIXME - should probably be asserting things in here, but exercising
        # the API is better than nothing.

        # Tidy up the files.
        os.remove(outfile)
        os.remove(outfile_routes)

    def test_fastplan_from_object(self):
        import djangobits.maps.models

        map_obj = djangobits.maps.models.MapObject(
            arrive_by=True,
            target_time=540,
            target_limit_time=0,
            target_e=393451,
            target_n=804639,
            )

        results = fastplanwrapper.fastplan_from_map_obj(
            shared_fastplan_pipe,
            map_obj,
            TMP_DIR,
            )
        print results

        # Tidy up files.
        os.remove(map_obj.temp_iso_file)
        os.remove(map_obj.temp_routes_file)

if __name__ == '__main__':
    with fastplanwrapper.SingleProcessFastPlan() as shared_fastplan_pipe:
        unittest.main()

