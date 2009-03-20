#
# Makefile:
# Build Contours of Life C++ journey planner.
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: francis@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: Makefile,v 1.10 2009-03-20 00:35:29 francis Exp $
#
#

CFLAGS = -Wall -O2 -fno-exceptions -fno-rtti
#CFLAGS = -Wall -O2 -DOUTPUT_ROUTE_DETAILS  # sometimes useful to output route details in release mode
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

