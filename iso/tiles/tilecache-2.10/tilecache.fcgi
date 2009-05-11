#!/usr/bin/python2.5

# Changes to work on pudding. Isochrones.py/Cones.py are level up,
# and pyproj is currently manually compiled. XXX
import sys

sys.path.extend(('../../../pylib', '..', '/home/matthew/lib/python'))

from TileCache.Service import wsgiApp

if __name__ == '__main__':
    from flup.server.fcgi_fork  import WSGIServer
    WSGIServer(wsgiApp).run()
