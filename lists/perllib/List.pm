#!/usr/bin/perl
#
# List.pm:
# List archive utilities.
#
# Copyright (c) 2006 UK Citizens Online Democracy. All rights reserved.
# Email: chris@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: List.pm,v 1.1 2006-07-09 15:42:54 chris Exp $
#

package List::DB;

use strict;

use mySociety::Config;
use mySociety::DBHandle qw(dbh);
use DBI;

BEGIN {
    mySociety::DBHandle::configure(
            Name => mySociety::Config::get('LIST_DB_NAME'),
            User => mySociety::Config::get('LIST_DB_USER'),
            Password => mySociety::Config::get('LIST_DB_PASS'),
            Host => mySociety::Config::get('LIST_DB_HOST', undef),
            Port => mySociety::Config::get('LIST_DB_PORT', undef)
        );
    # probably don't need a secret here
}

package List;

use strict;

1;
