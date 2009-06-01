
import os
import sys

filename = __file__
file_dir = os.path.abspath(os.path.dirname(filename))

sys.path.append(file_dir + "/../../../pylib")

import mysociety.config

mysociety.config.set_file(file_dir + "/../../conf/general")