#
# storage.py:
# Methods for storing and retreiving data for Contours of Life.
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: duncan@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: storage.py,v 1.8 2009-10-15 18:04:41 duncan Exp $
#

# Functions in this module should provide an API for accessing
# things that are stored, but in a way that means that the layers
# above don't need to know how things were stored.

import psycopg2

import psql_storage
import utils

class StorageError(Exception):
    """An error occurred when accessing storage."""

def get_invite_by_token(token_value):
    """
    Accepts token_value, a string, and returns a dictionary
    (I hope - I need to check that fetchone actually does what I 
    expect when used with DictCursor...) of keys/values for an invite,
    or None, if the invite wasn't found.
    """
    return psql_storage.get_invite_by_token(token_value)

def get_new_invites(email=None, source='friend', limit=1, debug=False):
    """
    This function returns the oldest invites with no token
    of type given by the source argument, up to a maximim given by limit.

    Called with an email address, this will return only invites to that email
    address.

    email - either an email address, or something false.
    source - currently either 'web' or 'friend', defaulting to 'friend'.
    limit - the maximum number of invites to return defaulting to 1
            so that we don't send a lot by accident.
    debug - boolean which determines how much is printed.
    """
    return psql_storage.get_new_invites(email=email,
                                        source=source,
                                        limit=limit,
                                        debug=debug)

def create_invite(email,
                  source='web',
                  source_id=None,
                  token=None):
    """
    Arguments are:

    email - an email address as a string
    source - a string describing what sort of invite this is. Currently
    expected values are: 'web', 'friend', or 'manual'.
    source_id - this will be an integer id of the person sending the invite
    if this is a friend invite, or None, if this is a web signup or manual
    invite.
    token - a token as a string, or None. If this is present, the invite is
    immediately active.

    This function does the following:
    1) Insert a new invite.
    2) Decrement the number of invites that the invitor has (if there is
    an invitor).
    3) Return that number of invites.
    """
    
    try:
        psql_storage.insert_invite(
            email, 
            source=source, 
            source_id=source_id,
            token=token
            )
    except psycopg2.IntegrityError:
        # Catch the database specific error and raise our own
        raise StorageError

    if source_id:
        # If this is an friend invite, then we need to decrement the source's invite count
        psql_storage.decrement_invite_count(source_id)

        # Return the number of invites left
        invite_row = psql_storage.get_invite_by_id(source_id)
        return invite_row['num_invites']

def set_invite_token(invite_id, token):
    """Accepts an invite_id and a token, and sets that token on the invite."""
    psql_storage.set_invite_token(invite_id, token)

def get_postcodes_by_invite(invite_id):
    """
    Accepts an invite_id (integer), and returns a list of 
    canonicalised postcodes (as strings) that are associated with that invite.
    """
    return [ (row['postcode'], utils.canonicalise_postcode(row['postcode']) ) for row in psql_storage.get_postcodes_by_invite(invite_id) ]

def add_postcode(invite_id, postcode):
    """
    Accepts an invite_id (integer) and a postcode (string) and stores that
    postcode against that invite.
    """
    psql_storage.add_postcode(invite_id, postcode)

def get_latest_postcodes(limit=10):
    """
    Fetches the last few postcodes which have complete maps.
    The optional argument limit is the maximum returned.
    """
    postcode_rows = psql_storage.get_latest_postcodes(limit=limit)

    return [ utils.canonicalise_postcode(row[0]) for row in postcode_rows ]

def get_nearest_station(easting, northing):
    """
    Accepts an easing and a northing, and returns the nearest station
    to those co-ordinates.
    Return value is a tuple of (text_id, long_description, id). 
    """
    return psql_storage.get_nearest_station(easting, northing)

def get_map_queue_state():
    return psql_storage.get_map_queue_state()

