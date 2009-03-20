#!/usr/bin/env python

# Changes to work on pudding. Isochrones.py/Cones.py are level up,
# and pyproj is currently manually compiled. XXX
import sys
sys.path.extend(('../../../pylib', '..', '/home/matthew/lib/python'))

from TileCache import Service, cgiHandler, cfgfiles

if __name__ == '__main__':
    svc = Service.load(*cfgfiles)
    cgiHandler(svc)

