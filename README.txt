

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
MOST PROJECTS ARE NOW IN GIT, CVS CONTAINS MAINLY HISTORICAL CODE NOW
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


mySociety source code
=====================

Here you can find the source code for various mySociety projects. This file
contains a description of the top level files and folders.

LICENSE.txt - Details of open source licensing terms, mainly the GNU Affero GPL
README-check - Run this to check everything is documented here


Still need moving to git
========================

orgsites - think of a better name :)
    ms - mySociety.org website
    ukcodwww - UKCOD.org.uk website
    cee - cee.mySociety.org website

internal - nobody else is likely to want to fork / hack on these
    intranet - Internal documentation / wiki
    secure - Development infrastructure, secure.mysociety.org
    ircwww - Internet Relay Chat web interface, www.irc.mysociety.org
    lists - Mailing lists
    piwik - Open source web analytics
    sitestats - Website statistics updates
    survey - Demographic etc. survey of users

internal-services
    services/EvEl - Email formatter and sender
    services/Ratty - Rate limit web page accesses
    services/DaDem - Look up who represents a given voting area (move to part of WriteToThem?)
    services/TilMa - Map tile server (move to part of FixMyStreet?)
    bbcparlvid - Parliamentary video (move to part of TheyWorkForYou?)

services/Gaze - Gazeteer, look up place names (runs under gaze.mysociety.org)

gny - Groups Near You
hm - HassleMe
scenic - Scenic or Not

monitoring - Our own server monitoring system
bin - General use scripts
misc
    rotatelogs - Enhanced rotatelogs program for apache
    run-with-lockfile - Lock a file and then execute a program
    pgblackbox - Records PostgreSQL action so can work out cause of deadlocks
    pnmtilesplit - Split a single large PNM file into numerous smaller tiles
    utils/mincore.c
    cpan/ - Various Perl modules packaged for CPAN


Historical but still live 
=========================

na - NotApathetic codebase
na2005 - NotApathetic 2005 UK General Election, static file version
cop - Comment on Power
placeopedia - Placeopedia
yhh - YourHistoryHere
news - Look up your local newspapers
services/NeWs - Directory of local newspapers
ideasbank - Guardian project
cvswww - Development infrastructure, cvs.mysociety.org
track - Conversion tracking (check nothing is using and turn off?)


Incomplete, dormant or non-mySociety projects
=============================================

ivfyb - I Voted For You Because
boxes - eDemocracy boxes for your website
gia - GiveItAway
panopticon - RSS aggregator
glocaliser - Glocaliser
rt - Modifications to Request Tracker
mscouk - mySociety.co.uk website
services/MaPit - Find voting areas for a given postcode (Matthew needs to CVS remove this)
meinedata - Flash widget for displaying graphical data
utils/dd.c
utils/dumpmem.c
utils/mailman_wrapper.c


Libraries etc. (use commonlib in git instead - these are old forks)
==============

perllib - General purpose Perl modules
phplib - General purpose PHP modules
pylib - General purpose Python modules
shlib - General purpose shell functions
jslib - General purpose javascript functions
rblib - General purpose Ruby functions
cpplib - General purpose C++ functions

