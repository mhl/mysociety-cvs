#
# psql_storage.py:
# Functions for storing and retreiving data for Contours of Life in postgresql.
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: duncan@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: psql_storage.py,v 1.28 2009-10-23 15:23:12 duncan Exp $
#

import functools
import psycopg2

from coldb import db
import storage_exceptions

def return_a_dict(func):
    """Decorate functions with this in order to return a dictionary
    rather than the half dictionary, half list thing that comes out of 
    DictCursor by default."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        nasty_row = func(*args, **kwargs)
        if nasty_row:
            return dict(nasty_row.items())

    return wrapper

class PSQLQueuedMap(object):
    def __init__(self, row):
        self._row = row

    def get_body(self):
        return self._row

    def release(self):
        self.db.execute("begin")
        self.db.execute("update map set state = 'new' where id = %(id)s", self._row)
        self.db.execute("commit")

    def delete(self):
        pass


class PSQLMapCreationQueue(object):
    def __init__(self, db_cursor=None):
        # At some point we should move to passing db_cursor in.
        self.db = db_cursor or db()

    def get_map_queue_state(self, map_id=None):
        state = { 'new': 0, 'working': 0, 'complete': 0, 'error' : 0 }
        self.db.execute('''SELECT state, count(*) FROM map GROUP BY state''')

        for row in self.db.fetchall():
            state[row[0]] = row[1]

        if map_id:
            self.db.execute('''SELECT count(*) as ahead_count FROM map WHERE created <= (SELECT created FROM map WHERE id = %s) AND state = 'new' ''', (map_id,))
            state['ahead'] = self.db.fetchone()['ahead_count']
            state['to_make'] = state['ahead'] + state['working']
        else:
            state['to_make'] = state['new'] + state['working'] + 1

        return state

    def queue_map(self, map_object):
        return insert_map(**map_object.__dict__)

    @return_a_dict
    def get_map_from_queue(self, server_description):
        # find something to do - we start with the map that was queued longest ago.
        offset = 0
        while True:
            try:
                self.db.execute("begin")
                # we get the row "for update" to lock it, and "nowait" so we
                # get an exception if someone else already has it, rather than
                # pointlessly waiting for them
                self.db.execute("""
    select
        id, 
        state, 
        (select text_id from station where id = target_station_id) as station_text_id, 
        target_e, 
        target_n,
        target_direction,
        target_time,
        target_limit_time,
        target_date 
    from map 
    where state = 'new' 
    order by created 
    limit 1 
    offset %s 
    for update nowait""" % offset)
                row = self.db.fetchone()
                break
            except psycopg2.OperationalError:
                # if someone else has the item locked, i.e. they are working on it, then we
                # try and find a different one to work on
                self.db.execute("rollback")
                offset = offset + 1
                #log("somebody else had the item, trying offset " + str(offset))
                continue

        # If there is nothing to do, then return.
        if not row:
            return

        map_id = row['id']
        state = row['state']
        # XXX check target_date here is same as whatever fastindex timetable file we're using

        # see if another instance of daemon got it *just* before us
        if state != 'new':
            #log("somebody else is already working on map " + str(id))
            self.db.execute("rollback")
            return

        # recording in the database that we are working on this
        #log("working on map " + str(id))
        self.db.execute("update map set state = 'working', working_server = %(server)s, working_start = now() where id = %(id)s", 
                dict(id=map_id, server=server_description))
        self.db.execute("commit")

        queued_map = PSQLQueuedMap(**row)

        return queued_map


@return_a_dict
def get_invite_by_token(token_value):
    if token_value:
        db().execute('SELECT * FROM invite WHERE token=%s', (token_value,))
        return db().fetchone()

@return_a_dict
def get_invite_by_id(invite_id):
    db().execute('SELECT * FROM invite WHERE id=%s', (invite_id,))
    return db().fetchone()

def get_new_invites(email=None, limit=1, source=None, debug=False):
    if source == 'web':
        query = 'SELECT * FROM invite WHERE token IS NULL AND invite.source_id IS NULL'
    elif source == 'friend':
        query = 'SELECT invite.*, inviter.email as inviter_email FROM invite, invite as inviter WHERE invite.source_id = inviter.id AND invite.token IS NULL'
        
    if email:
        query = query + " AND invite.email = '%s'" % (email)
    query = query + ' ORDER BY invite.id'
    
    if limit:
        query = query + ' LIMIT %s' % (limit)

    if debug:
        print "Query:", query

    db().execute(query)

    return db().fetchall()

def insert_invite(email,
                  source='web',
                  source_id=None,
                  token=None):

    db().execute('BEGIN')

    try:
        db().execute("INSERT INTO invite (email, source, source_id, token) VALUES (%s, %s, %s, %s)", (email, source, source_id, token))
        db().execute('COMMIT')
    except psycopg2.IntegrityError:
        # Let's assume the integrity error is because of a unique key
        # violation - ie. an identical row has appeared in the milliseconds
        # since we looked
        db().execute('ROLLBACK')

        raise

def decrement_invite_count(invite_id):
    db().execute('UPDATE invite SET num_invites = num_invites - 1 WHERE id=%s', (invite_id,))
    db().execute('COMMIT')
    
def set_invite_token(invite_id, token):
    db().execute('UPDATE invite SET token=%s where id=%s', (token, invite_id))
    db().execute('COMMIT')

def get_postcodes_by_invite(invite_id, limit=100):    
    db().execute('SELECT postcode FROM invite_postcode WHERE invite_id=%s ORDER BY id DESC LIMIT %s', (invite_id, limit))
    return db().fetchall()

def add_postcode(invite_id, postcode):
    db().execute('''INSERT INTO invite_postcode (invite_id, postcode) VALUES (%s, '%s')''' % (invite_id, postcode))
    db().execute('COMMIT')

def get_latest_postcodes(limit=10):
    db().execute('''SELECT target_postcode FROM map WHERE state='complete' AND target_postcode IS NOT NULL
        ORDER BY working_start DESC LIMIT %s''' %limit)
    return db().fetchall()

# Find station nearest to given easting/northing
@return_a_dict
def get_nearest_station(easting, northing):
    db().execute('''SELECT text_id, long_description, id FROM station WHERE
        position_osgb && Expand(GeomFromText('POINT(%(easting)s %(northing)s)', 27700), 50000)
        AND Distance(position_osgb, GeomFromText('POINT(%(easting)s %(northing)s)', 27700)) < 50000
        ORDER BY Distance(position_osgb, GeomFromText('POINT(%(easting)s %(northing)s)', 27700))
        LIMIT 1''' %{'easting':easting, 'northing':northing})
    return db().fetchone()

@return_a_dict
def get_station_coords(station_id):
    db().execute('''SELECT id, X(position_osgb), Y(position_osgb) FROM station WHERE text_id = %s''', (station_id,))
    return db().fetchone()

def insert_map(**kwargs):
    try:
        db().execute('BEGIN')
        db().execute("SELECT nextval('map_id_seq') as next_map_id")

        map_id = db().fetchone()['next_map_id']
        params = {'id': map_id}
        params.update(kwargs)

        try:
            db().execute('INSERT INTO map (id, state, working_server, working_start, working_took, target_station_id, target_postcode, target_e, target_n, target_direction, target_time, target_limit_time, target_date) VALUES (%(id)s, %(state)s, %(target_station_id)s, %(target_postcode)s, %(target_e)s, %(target_n)s, %(target_direction)s, %(target_time)s, %(target_limit_time)s, %(target_date)s)', params)

        except:
            db().execute('ROLLBACK')
            raise

        db().execute('COMMIT')

    except psycopg2.IntegrityError, e:
        if e.pgcode == psycopg2.errorcodes.UNIQUE_VIOLATION:
            # The integrity error is because of a unique key violation - ie. an
            # identical row has appeared in the milliseconds since we looked
            raise storage_exceptions.AlreadyQueuedError
        else:
            raise

    return map_id


def notify_map_done(map_id, time_taken):
    db().execute("begin")
    db().execute("update map set state = 'complete', working_took = %(took)s where id = %(id)s", dict(id=map_id, took=time_taken))
    db().execute("commit")

def notify_map_error(map_id):
    db().execute("begin")
    db().execute("update map set state = 'error' where id = %(id)s", dict(id=map_id))
    db().execute("commit")
    
@return_a_dict
def get_map_status_by_position(
    easting,
    northing,
    direction,
    target_time,
    limit_time,
    target_date,
    ):
    """Returns the id of the map, the current state, and the server working
    on it (as a tuple) if it is queued, or None, if not."""

    db().execute('''SELECT id, state, working_server FROM map WHERE 
                target_e = %s AND target_n = %s AND 
                target_direction = %s AND
                target_time = %s AND target_limit_time = %s 
                AND target_date = %s''', 
                 (easting, northing, direction, 
                  target_time, limit_time, target_date)
                 )
    return db().fetchone()

@return_a_dict
def get_map_status_by_station(
    station_id,
    direction,
    target_time,
    limit_time,
    target_date,
    ):
    """Returns the id of the map, the current state, and the server working
    on it (as a tuple) if it is queued, on None, if not."""

    db().execute('''SELECT id, state, working_server FROM map WHERE 
                target_station_id = %s AND 
                target_direction = %s AND
                target_time = %s AND target_limit_time = %s 
                AND target_date = %s''', 
                 (station_id, direction, 
                  target_time, limit_time, target_date)
                 )
    return db().fetchone()
    
def get_average_generation_time(
    target_direction=None,
    target_time=None,
    target_limit_time=None,
    target_date=None,
    ):
    # Take average time for maps with the same times, taken from the last
    # day, or last 50 at most.
    # XXX will need to make times ranges if we let people enter any time in UI
    db().execute('''SELECT AVG(working_took) as average_time FROM 
        ( SELECT working_took FROM map WHERE
            target_direction = %s AND
            target_time = %s AND target_limit_time = %s AND target_date = %s AND
            working_start > (SELECT MAX(working_start) FROM map) - '1 day'::interval 
            ORDER BY working_start DESC LIMIT 50
        ) AS working_took
        ''', 
        (target_direction, target_time, target_limit_time, target_date))
    row = db().fetchone()

    avg_time = row['average_time'] if row else None

    return avg_time or 30



def queue_map_email(email_address, map_id):
    """Accepts an email address and a map_id and queues an 
    email about that map to that email address.
    """
    db().execute('BEGIN')
    db().execute('INSERT INTO email_queue (email, map_id) VALUES (%s, %s)', (email_address, map_id))
    db().execute('COMMIT')
