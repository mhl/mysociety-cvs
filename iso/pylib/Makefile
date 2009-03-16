#
# Makefile:
# Build Contours of Life C++ journey planner.
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: francis@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: Makefile,v 1.5 2009-03-16 01:18:38 francis Exp $
#
#

CFLAGS = -Wall -O2 -fno-rtti -fno-exceptions
CFLAGS_DEBUG = -Wall -g -DDEBUG
CFLAGS_PROFILE = -Wall -pg

CPP = /usr/bin/g++

all: makeplan

makeplan: makeplan.cpp Makefile
	$(CPP) $(CFLAGS) makeplan.cpp -o makeplan

makeplan-debug: makeplan.cpp Makefile
	$(CPP) $(CFLAGS_DEBUG) makeplan.cpp -o makeplan-debug

makeplan-profile: makeplan.cpp Makefile
	$(CPP) $(CFLAGS_PROFILE) makeplan.cpp -o makeplan-profile

clean:
	rm -f makeplan core

