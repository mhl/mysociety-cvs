import unittest
import os

import s3_models

class TestS3Storage(unittest.TestCase):
    def test_store_and_delete(self):
        testfilename = 'test_store_and_delete'

        # FIXME - should probably use a temporary directory for this
        # Create a file to store
        testfile = open(testfilename, 'w')
        testfile.write('Testing!')
        testfile.close()

        s3_models.store_file(key_name=testfilename,
                             file_location=testfilename,
                             delete_file=True)

        # Can't see an easy way to check that the 

if __name__ == '__main__':
    import sys
    sys.path.append('../../../../pylib/')
    
    import mysociety.config
    mysociety.config.set_file("../../../conf/unittest")
    
    unittest.main()
