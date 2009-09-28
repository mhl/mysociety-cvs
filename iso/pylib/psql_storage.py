#
# psql_storage.py:
# Functions for storing and retreiving data for Contours of Life in postgresql.
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: duncan@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: psql_storage.py,v 1.2 2009-09-28 14:04:32 duncan Exp $
#

# Functions is this module should return rows in the format that
# psycopg2 uses.

import psycopg2

from coldb import db


def get_invite_by_token(token_value):
    db().execute('SELECT * FROM invite WHERE token=%s', (token_value,))
    return db().fetchone()

def get_invite_by_id(invite_id):
    db().execute('SELECT * FROM invite WHERE id=%s', (invite_id,))
    return db().fetchone()

def insert_invite(email,
                  source='web',
                  source_id=None):

    db().execute('BEGIN')

    try:
        db().execute("INSERT INTO invite (email, source, source_id) VALUES (%s, %s, %s)", (email, source, source_id))
    except psycopg2.IntegrityError:
        # Let's assume the integrity error is because of a unique key
        # violation - ie. an identical row has appeared in the milliseconds
        # since we looked
        db().execute('ROLLBACK')

        raise

def decrement_invite_count(invite_id):
    db().execute('UPDATE invite SET num_invites = num_invites - 1 WHERE id=%s', (invite_id,))
    db().execute('COMMIT')
    
def get_postcodes_by_invite(invite_id, limit=100):    
    db().execute('SELECT postcode FROM invite_postcode WHERE invite_id=%d ORDER BY id DESC LIMIT %d', (invite_id, limit))
    return db().fetchall()

def add_postcode(invite_id, postcode):
    db().execute('''INSERT INTO invite_postcode (invite_id, postcode) VALUES (%d, '%d')''' % (invite_id, postcode))
    db().execute('COMMIT')

def get_latest_postcodes(limit=10):
    db().execute('''SELECT target_postcode FROM map WHERE state='complete' AND target_postcode IS NOT NULL
        ORDER BY working_start DESC LIMIT %d''' %limit)
    return db().fetchall()

# Find station nearest to given easting/northing
def get_nearest_station(easting, northing):
    db().execute('''SELECT text_id, long_description, id FROM station WHERE
        position_osgb && Expand(GeomFromText('POINT(%d %d)', 27700), 50000)
        AND Distance(position_osgb, GeomFromText('POINT(%d %d)', 27700)) < 50000
        ORDER BY Distance(position_osgb, GeomFromText('POINT(%d %d)', 27700))
        LIMIT 1''' % (easting, northing, easting, northing, easting, northing))
    return db().fetchone()
