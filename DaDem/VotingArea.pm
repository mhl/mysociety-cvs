#!/usr/bin/perl
#
# VotingArea.pm:
# Voting area definitions.
#
# Copyright (c) 2004 UK Citizens Online Democracy. All rights reserved.
# Email: chris@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: VotingArea.pm,v 1.1 2004-10-06 15:41:23 chris Exp $
#

package VotingArea;

use constant LBO => 101; # London Borough
use constant LBW => 102; # ... ward

use constant GLA => 201; # Greater London Assembly
use constant LAC => 202; # London constituency

use constant CTY => 301; # County
use constant CED => 302; # ... electoral division

use constant DIS => 401; # District
use constant DIW => 402; # ... ward

use constant UTA => 501; # Unitary authority
use constant UTE => 502; # ... electoral division
use constant UTW => 503; # ... ward

use constant MTD => 601; # Metropolitan district
use constant MTW => 602; # ... ward

use constant SPA => 701; # Scottish Parliament
use constant SPE => 702; # ... electoral region
use constant SPC => 703; # ... constituency

use constant WAS => 701; # Welsh Assembly
use constant WAE => 702; # ... electoral region
use constant WAC => 702; # ... constituency

use constant WMP => 801; # Westminster Parliament
use constant WMC => 802; # ... constituency

use constant EUP => 901; # European Parliament
use constant EUR => 902; # ... region


1;
