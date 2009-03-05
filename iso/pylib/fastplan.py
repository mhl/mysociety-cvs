#
# fastplan.py:
# Ouputs data structure for use making plans, as makeplan.py, but from a faster
# separate C++ programme.
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: francis@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: fastplan.py,v 1.1 2009-03-05 16:04:18 francis Exp $
#

import logging
import datetime
import sys
import os
import math

sys.path.append(sys.path[0] + "/../../pylib") # XXX this is for running doctests and is nasty, there's got to be a better way
import mysociety.atcocif
      
class FastPregenATCO(mysociety.atcocif.ATCO):
    def __init__(self):
        pass

if __name__ == "__main__":
    import doctest
    doctest.testmod()

