#
# Makefile:
# Build 
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: francis@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: Makefile,v 1.1 2009-03-13 09:36:25 francis Exp $
#

CFLAGS = -Wall -g -O2
LDFLAGS =
LDLIBS = 
CPP = /usr/bin/g++

all: makeplan

makeplan: makeplan.cpp Makefile
	$(CPP) $(CFLAGS) makeplan.cpp -o makeplan

clean:
	rm -f makeplan core

