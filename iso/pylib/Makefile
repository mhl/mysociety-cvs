#
# Makefile:
# Build Contours of Life C++ journey planner.
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: francis@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: Makefile,v 1.3 2009-03-13 16:28:49 francis Exp $
#
#

CFLAGS = -Wall -O2 -fno-rtti -fno-exceptions
CFLAGS_DEBUG = -Wall -g -DDEBUG

CPP = /usr/bin/g++

all: makeplan

makeplan: makeplan.cpp Makefile
	$(CPP) $(CFLAGS) makeplan.cpp -o makeplan

makeplan-debug: makeplan.cpp Makefile
	$(CPP) $(CFLAGS_DEBUG) makeplan.cpp -o makeplan-debug

clean:
	rm -f makeplan core

