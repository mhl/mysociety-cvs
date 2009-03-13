#
# Makefile:
# Build Contours of Life C++ journey planner.
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: francis@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: Makefile,v 1.2 2009-03-13 11:23:45 francis Exp $
#

CFLAGS = -Wall -g -O2
CPP = /usr/bin/g++

all: makeplan

makeplan: makeplan.cpp Makefile
	$(CPP) $(CFLAGS) makeplan.cpp -o makeplan

clean:
	rm -f makeplan core

