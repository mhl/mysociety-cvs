#
# Makefile:
# Build Contours of Life C++ journey planner.
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: francis@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: Makefile,v 1.4 2009-03-24 17:20:00 francis Exp $
#

CFLAGS = -Wall -O2 -fno-exceptions -fno-rtti
CFLAGS_WITH_ROUTE = -Wall -O2 -DOUTPUT_ROUTE_DETAILS 
CFLAGS_DEBUG = -Wall -g -DDEBUG -DOUTPUT_ROUTE_DETAILS
CFLAGS_PROFILE = ${CFLAGS} -pg

FASTPLAN_BINARIES=fastplan fastplan-with-route fastplan-debug fastplan-profile
FASTPLAN_COOPT_BINARIES=fastplan-coopt

CPP = /usr/bin/g++

all: ${FASTPLAN_BINARIES} ${FASTPLAN_COOPT_BINARIES}

clean:
	rm -f ${FASTPLAN_BINARIES} ${FASTPLAN_COOPT_BINARIES}

#########################################################################
# Command line planner, called by do-nptdr.py

fastplan: fastplan.cpp Makefile
	$(CPP) $(CFLAGS) fastplan.cpp -o fastplan

fastplan-with-route: fastplan.cpp Makefile
	$(CPP) $(CFLAGS_WITH_ROUTE) fastplan.cpp -o fastplan-with-route

fastplan-debug: fastplan.cpp Makefile
	$(CPP) $(CFLAGS_DEBUG) fastplan.cpp -o fastplan-debug

fastplan-profile: fastplan.cpp Makefile
	$(CPP) $(CFLAGS_PROFILE) fastplan.cpp -o fastplan-profile

#########################################################################
# Special version of planner for Python daemon to talk to

fastplan-coopt: fastplan-coopt.cpp Makefile
	$(CPP) $(CFLAGS) fastplan-coopt.cpp -o fastplan-coopt


