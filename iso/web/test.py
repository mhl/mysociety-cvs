#!/usr/bin/python2.5

# test.py:
# Test web code for Contours of Life.
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: francis@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: test.py,v 1.1 2009-06-03 18:47:07 francis Exp $
#

import doctest
import imp

def test_cgis():
    # You can't just import .cgi files because they don't have a .py function.
    # User lower level imp.load_module to do the import instead.
    index = imp.load_module('index', open('index.cgi'), 'index.cgi', ('.cgi', 'U', imp.PY_SOURCE))
    doctest.testmod(index)

if __name__ == '__main__':
    test_cgis()

