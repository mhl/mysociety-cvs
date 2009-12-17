#
# aws_storage.py:
# Functions for storing and retreiving data for Contours of Life in Amazon Web Services.
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: duncan@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: aws_storage.py,v 1.8 2009-12-17 16:27:30 duncan Exp $
#

import sys
sys.path.extend(("../pylib", "../../pylib"))

import datetime

# This is the rather stupidly named Amazon Web Services module.
import boto.sqs.connection
import boto.sqs.message

import mysociety.config

aws_connection = boto.sqs.connection.SQSConnection(
    mysociety.config.get('AWS_KEY'),
    mysociety.config.get('AWS_SECRET'),
    )

import maps.models

# FIXME - should make the queue visibility timeout an option

def get_or_create_queue(queue_name, visibility_timeout):
    # Get the queue with this name if it exists, or create it if not.

    queue = aws_connection.lookup(queue_name)

    if queue:
        queue.set_timeout(visibility_timeout)
    else:
        queue = aws_connection.create_queue(queue_name, visibility_timeout)
    
    return queue

class CantQueueError(Exception):
    """For some reason the map could not be added to the queue."""

class AWSMapCreationQueue(object):
    def __init__(self, queue_name, visibility_timeout):
        self.queue = get_or_create_queue(queue_name, visibility_timeout)

    def get_map_queue_state(self, map_id=None):
        # FIXME - This method will need info from more than just the queue
        # Will probably need to take it off this class.
        
        # This is a stub which returns something to display so that things don't break
        return { 'new': 0, 'working': 0, 'complete': 0, 'error' : 0, 'to_make': 0 }

    def queue_map(self, map_object):
        # FIXME - These comments are useful, but should now be somewhere else.
        # We need a key to name the map with in either the filestore or AWS
        # How about combining together all the attributes that make a map
        # unique: station_id, target_e, target_n, direction, time, limit_time

        # So what exactly do all these things look like?
        # station_id: a string of A-Z0-9 (often this will be the empty string)
        # target_e: an int (OSGB fully numeric, by the look of it, up to 6 digits)
        # target_n: an int (OSGB fully numeric, up to 7 digits - if you get near Orkney).
        # direction: arrive_by or depart_after (we can store this as 'a' or 'd')
        # time: an integer of minutes since midnight (maximum 1439)
        # limit_time: an integer of minutes since midnight (maximum 1439)

        # None of these contains an underscore: let's make a key by joining
        # them in order with underscores.

        # Note that the map is being queued
        map_object.queued_at = datetime.datetime.now()
        map_object.save()
        # This save will ensure that the map has an identifier.

        # Do the actual queueing.
        message = boto.sqs.message.Message()
        message.set_body(map_object.identifier)
        success = self.queue.write(message)
        
        if not success:
            raise CantQueueError("For some reason the queue didn't accept the message.")
            

        # FIXME - what is this return value used for? Does this need to return
        # anything?
        #return map_id

    def get_map_from_queue(self, server_description=None):
        message = self.queue.read()

        if message:
            # FIXME - this will raise an error if the item doesn't exist.
            # we should be prepared and catch it.
            map_object = maps.models.MapObject.objects.get(message.get_body())
            map_object.set_queue_message(message)
            return map_object
