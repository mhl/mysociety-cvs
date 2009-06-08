
import os
import sys
filename = __file__
package_dir = os.path.abspath(os.path.dirname(filename))
sys.path.append(package_dir + "/../../../pylib")
import mysociety.config
mysociety.config.set_file(package_dir + "/../../conf/general")
