#
# Makefile:
# Build Contours of Life C++ journey planner.
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: francis@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: Makefile,v 1.7 2009-03-26 11:08:57 francis Exp $
#

CFLAGS = -Wall -O2 -fno-exceptions -fno-rtti
CFLAGS_WITH_ROUTE = -Wall -O2 -DOUTPUT_ROUTE_DETAILS 
CFLAGS_DEBUG = -Wall -g -DDEBUG -DOUTPUT_ROUTE_DETAILS
CFLAGS_PROFILE = ${CFLAGS} -pg

BINARIES=fastplan fastplan-with-route fastplan-debug fastplan-profile fastplan-coopt fastplan-coopt-debug stationlist

CPP = /usr/bin/g++

all: ${BINARIES}

clean:
	rm -f ${BINARIES}

#########################################################################
# Command line planner, called by do-nptdr.py

FASTPLAN_DEPEND=fastplan.cpp Makefile ../cpplib/makeplan.h ../cpplib/performance_monitor.h ../../cpplib/mysociety_error.h

fastplan: ${FASTPLAN_DEPEND}
	$(CPP) $(CFLAGS) fastplan.cpp -o fastplan

fastplan-with-route: ${FASTPLAN_DEPEND}
	$(CPP) $(CFLAGS_WITH_ROUTE) fastplan.cpp -o fastplan-with-route

fastplan-debug: ${FASTPLAN_DEPEND} 
	$(CPP) $(CFLAGS_DEBUG) fastplan.cpp -o fastplan-debug

fastplan-profile: ${FASTPLAN_DEPEND}
	$(CPP) $(CFLAGS_PROFILE) fastplan.cpp -o fastplan-profile

#########################################################################
# Special version of planner for Python daemon to talk to

FASTPLAN_COOPT_DEPEND=fastplan-coopt.cpp Makefile ../cpplib/makeplan.h ../../cpplib/mysociety_error.h

fastplan-coopt: ${FASTPLAN_COOPT_DEPEND}
	$(CPP) $(CFLAGS) fastplan-coopt.cpp -o fastplan-coopt

fastplan-coopt-debug: ${FASTPLAN_COOPT_DEPEND}
	$(CPP) $(CFLAGS_DEBUG) fastplan-coopt.cpp -o fastplan-coopt-debug

#########################################################################
# Just outputs list of stations and connectivity measure

stationlist: stationlist.cpp Makefile ../cpplib/makeplan.h ../../cpplib/mysociety_error.h
	$(CPP) $(CFLAGS) stationlist.cpp -o stationlist


