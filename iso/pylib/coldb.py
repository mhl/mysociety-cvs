#
# coldb.py:
# Database connection for Contours of Life.
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: francis@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: coldb.py,v 1.6 2009-06-04 10:37:51 francis Exp $
#

import sys
import psycopg2
import psycopg2.extras

sys.path.append("../../pylib")
import mysociety.config

# Make new connections
def get_connection():
    return psycopg2.connect(
            host=mysociety.config.get('COL_DB_HOST'),
            port=mysociety.config.get('COL_DB_PORT'),
            database=mysociety.config.get('COL_DB_NAME'),
            user=mysociety.config.get('COL_DB_USER'),
            password=mysociety.config.get('COL_DB_PASS')
    )
 
def get_cursor(connection = None):
    if not connection:
        connection = get_connection()
    return connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

# Global database
global_db = None
def db():
    global global_db
    if not global_db:
        global_db = get_cursor()
    return global_db

