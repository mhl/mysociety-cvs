#
# Makefile:
# Build Contours of Life C++ journey planner.
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: francis@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: Makefile,v 1.9 2009-03-17 16:43:19 francis Exp $
#
#

# OUTPUT_ROUTE_DETAILS shaves a few seconds off full country map generation,
# including that it allows no-exceptions no-rtti as it removes boost format
# dependency. For now though, don't worry about it too much.

CFLAGS = -Wall -O2 -DOUTPUT_ROUTE_DETAILS 
#CFLAGS = -Wall -O2 -fno-exceptions -fno-rtti
CFLAGS_DEBUG = -Wall -g -DDEBUG -DOUTPUT_ROUTE_DETAILS
CFLAGS_PROFILE = ${CFLAGS} -pg

CPP = /usr/bin/g++

all: makeplan makeplan-debug makeplan-profile

makeplan: makeplan.cpp Makefile
	$(CPP) $(CFLAGS) makeplan.cpp -o makeplan

makeplan-debug: makeplan.cpp Makefile
	$(CPP) $(CFLAGS_DEBUG) makeplan.cpp -o makeplan-debug

makeplan-profile: makeplan.cpp Makefile
	$(CPP) $(CFLAGS_PROFILE) makeplan.cpp -o makeplan-profile

clean:
	rm -f makeplan core

