#
# storage.py:
# Methods for storing and retreiving data for Contours of Life.
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: duncan@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: storage.py,v 1.14 2009-10-20 16:47:56 duncan Exp $
#

# Functions in this module should provide an API for accessing
# things that are stored, but in a way that means that the layers
# above don't need to know how things were stored.

import psycopg2
import psycopg2.errorcodes

import psql_storage
import utils

class StorageError(Exception):
    """An error occurred when accessing storage."""

class AlreadyQueuedError(Exception):
    """The details asked for are already in the queue."""

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

def get_station_coords(station_text_id):
    """Accepts a station text id, and returns a triple of station_id, 
    easting and northing."""
    return psql_storage.get_station_coords(station_text_id)

def get_map_queue_state(map_id=None):
    """Returns a dictionary with keys 

    'new', 'working', 'complete', 'error', 'to_make'

    each of which stores the number of maps in that state as its value.

    If the optional argument map_id is passed in, there will also be a
    key 'ahead' showing how many maps are ahead of this one in the queue.
    """
    return psql_storage.get_map_queue_state(map_id)

def queue_map(
    target_station_id=None, 
    target_postcode=None, 
    target_e=None,
    target_n=None,
    target_direction=None,
    target_time=None,
    target_limit_time=None,
    target_date=None,
    ):
    """Queue up a map with the attributes passed in.

    Returns a unique id for the map which can be used in filenames, etc.
    """
    try:
        return psql_storage.queue_map(
            target_station_id=target_station_id, 
            target_postcode=target_postcode, 
            target_e=target_e,
            target_n=target_n,
            target_direction=target_direction,
            target_time=target_time,
            target_limit_time=target_limit_time,
            target_date=target_date,
            )

    except psycopg2.IntegrityError, e:
        if e.pgcode == psycopg2.errorcodes.UNIQUE_VIOLATION:
            # The integrity error is because of a unique key violation - ie. an
            # identical row has appeared in the milliseconds since we looked
            raise AlreadyQueuedError
        else:
            raise

def get_map_from_queue(server_description):
    """
    Takes a variable server_description, which is used to record who is 
    working on this item in the queue.

    Returns a tuple:

    (id, state, target_station_text_id, target_e, target_n, target_direction, target_time, target_limit_time, target_date)

    of a map that needs making.
    """
    return psql_storage.get_map_from_queue(server_description)

def return_map_to_queue(map_id):
    """For some reason we've not finished working on this map properly,
    so put it back in the queue."""
    psql_storage.return_map_to_queue(map_id)

def drop_map_from_queue(map_id):
    """Notify the queue that this map doesn't need doing any more."""
    # At the moment we don't need this, as it's handled in notify_map_done.

def notify_map_done(map_id, time_taken):
    """Notify the front end that the map is done."""
    psql_storage.notify_map_done(map_id, time_taken)

def notify_map_error(map_id):
    """Notify the front end that a map has failed."""
    psql_storage.notify_map_error(map_id)

def get_map_status(
    direction,
    target_time,
    limit_time,
    target_date,
    easting=None,
    northing=None,
    station_id=None,
    ):
    """Returns the id of the map, the current state, and the server working
    on it (as a tuple) if it is queued, or None, if not.

    Requires inputs of direction, target_time, limit_time, target_date, and
    either both easting and northing or station_id
    """

    common_args = (direction, target_time, limit_time, target_date)

    if station_id:
        return psql_storage.get_map_status_by_station(station_id, *common_args)
            
    elif easting and northing:
        psql_storage.get_map_status_by_position(easting, northing, *common_args)
    else:
        raise Exception('Insufficient info to find map.')

def get_average_generation_time(
    target_direction=None,
    target_time=None,
    target_limit_time=None,
    target_date=None,
    ):
    """Returns the expected waiting time for a similar sort of map.
    """
    return psql_storage.get_average_generation_time(
        target_direction=target_direction,
        target_time=target_time,
        target_limit_time=target_limit_time,
        target_date=target_date,
        )

def queue_map_email(email_address, map_id):
    """Accepts an email address and a map_id and queues an 
    email about that map to that email address.
    """
    psql_storage.queue_map_email(email_address, map_id)
    
