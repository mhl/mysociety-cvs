#
# coldb.py:
# Database connection for Contours of Life.
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: francis@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: coldb.py,v 1.2 2009-04-22 13:16:01 francis Exp $
#

import sys
import psycopg2 as postgres

sys.path.append("../../pylib")
import mysociety.config

def get_cursor():
    return postgres.connect(
            host=mysociety.config.get('COL_DB_HOST'),
            port=mysociety.config.get('COL_DB_PORT'),
            database=mysociety.config.get('COL_DB_NAME'),
            user=mysociety.config.get('COL_DB_USER'),
            password=mysociety.config.get('COL_DB_PASS')
    ).cursor()

