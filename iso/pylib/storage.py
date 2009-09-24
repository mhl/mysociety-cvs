#
# storage.py:
# Methods for storing and retreiving data for Contours of Life.
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: duncan@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: storage.py,v 1.1 2009-09-24 15:09:41 duncan Exp $
#

from coldb import db
from psycopg2 import IntegrityError

class StorageError(Exception):
    """An error occurred when accessing storage."""

def token_exists(token):
    db().execute('SELECT * FROM invite WHERE token=%s', (token,))
    return db().fetchone()

def create_invite(email,
                  source='web',
                  source_id=None):

    db().execute('BEGIN')

    try:
        db().execute("INSERT INTO invite (email, source, source_id) VALUES (%s, %s, %s)", (email, source, source_id))
    except IntegrityError, e:
        # Let's assume the integrity error is because of a unique key
        # violation - ie. an identical row has appeared in the milliseconds
        # since we looked
        db().execute('ROLLBACK')

        raise StorageError

    if source_id:
        # If this is an friend invite, then we need to decrement the source's invite count
        db().execute('UPDATE invite SET num_invites = num_invites - 1 WHERE id=%s', (source_id,))
        db().execute('COMMIT')

        db().execute('SELECT num_invites FROM invite WHERE id=%s', (source_id,))
        num = db().fetchone()[0]

        # Return the number of invites left.
        return num
