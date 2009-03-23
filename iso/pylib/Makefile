#
# Makefile:
# Build Contours of Life C++ journey planner.
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: francis@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: Makefile,v 1.14 2009-03-23 08:44:46 francis Exp $
#

CFLAGS = -Wall -O2 -fno-exceptions -fno-rtti
CFLAGS_WITH_ROUTE = -Wall -O2 -DOUTPUT_ROUTE_DETAILS 
CFLAGS_DEBUG = -Wall -g -DDEBUG -DOUTPUT_ROUTE_DETAILS
CFLAGS_PROFILE = ${CFLAGS} -pg

CPP = /usr/bin/g++

all: makeplan makeplan-with-route makeplan-debug makeplan-profile

makeplan: makeplan.cpp Makefile
	$(CPP) $(CFLAGS) makeplan.cpp -o makeplan

makeplan-with-route: makeplan.cpp Makefile
	$(CPP) $(CFLAGS_WITH_ROUTE) makeplan.cpp -o makeplan-with-route

makeplan-debug: makeplan.cpp Makefile
	$(CPP) $(CFLAGS_DEBUG) makeplan.cpp -o makeplan-debug

makeplan-profile: makeplan.cpp Makefile
	$(CPP) $(CFLAGS_PROFILE) makeplan.cpp -o makeplan-profile

clean:
	rm -f makeplan makeplan-with-route makeplan-debug makeplan-profile core

