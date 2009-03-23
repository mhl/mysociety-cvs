#
# Makefile:
# Build Contours of Life C++ journey planner.
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: francis@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: Makefile,v 1.3 2009-03-23 09:30:07 francis Exp $
#

CFLAGS = -Wall -O2 -fno-exceptions -fno-rtti
CFLAGS_WITH_ROUTE = -Wall -O2 -DOUTPUT_ROUTE_DETAILS 
CFLAGS_DEBUG = -Wall -g -DDEBUG -DOUTPUT_ROUTE_DETAILS
CFLAGS_PROFILE = ${CFLAGS} -pg

CPP = /usr/bin/g++

all: fastplan fastplan-with-route fastplan-debug fastplan-profile

fastplan: fastplan.cpp Makefile
	$(CPP) $(CFLAGS) fastplan.cpp -o fastplan

fastplan-with-route: fastplan.cpp Makefile
	$(CPP) $(CFLAGS_WITH_ROUTE) fastplan.cpp -o fastplan-with-route

fastplan-debug: fastplan.cpp Makefile
	$(CPP) $(CFLAGS_DEBUG) fastplan.cpp -o fastplan-debug

fastplan-profile: fastplan.cpp Makefile
	$(CPP) $(CFLAGS_PROFILE) fastplan.cpp -o fastplan-profile

clean:
	rm -f fastplan fastplan-with-route fastplan-debug fastplan-profile core

