#
# storage.py:
# Methods for storing and retreiving data for Contours of Life.
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: duncan@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: storage.py,v 1.4 2009-09-28 10:10:42 duncan Exp $
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

def create_invite(email,
                  source_id=None):
    """
    Arguments are:

    email - an email address as a string
    source_id - this will be an integer id of the person sending the invite
    if this is a friend invite, or None, if this is a web signup.

    This function does the following:
    1) Insert a new invite.
    2) Decrement the number of invites that the invitor has.
    3) Return that number of invites.
    """

    try:
        psql_storage.insert_invite(
            email, 
            source='friend' if source_id else 'web', 
            source_id=source_id
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
