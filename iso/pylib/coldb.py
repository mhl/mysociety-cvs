#
# coldb.py:
# Database connection for Contours of Life.
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: francis@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: coldb.py,v 1.3 2009-04-27 15:33:31 francis Exp $
#

import sys
import psycopg2

sys.path.append("../../pylib")
import mysociety.config

def get_cursor():
    return psycopg2.connect(
            host=mysociety.config.get('COL_DB_HOST'),
            port=mysociety.config.get('COL_DB_PORT'),
            database=mysociety.config.get('COL_DB_NAME'),
            user=mysociety.config.get('COL_DB_USER'),
            password=mysociety.config.get('COL_DB_PASS')
    ).cursor()

