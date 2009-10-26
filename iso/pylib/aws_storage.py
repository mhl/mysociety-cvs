#
# aws_storage.py:
# Functions for storing and retreiving data for Contours of Life in Amazon Web Services.
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: duncan@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: aws_storage.py,v 1.5 2009-10-26 15:26:24 duncan Exp $
#

import sys
sys.path.extend(("../pylib", "../../pylib"))

import pickle

# This is the rather stupidly named Amazon Web Services module.
import boto.sqs.connection
import boto.sqs.message

import mysociety.config
mysociety.config.set_file("../conf/general")

aws_connection = boto.sqs.connection.SQSConnection(
    mysociety.config.get('AWS_KEY'),
    mysociety.config.get('AWS_SECRET'),
    )

# FIXME - should make the queue visibility timeout an option

def get_or_create_queue(queue_name, visibility_timeout):
    # Get the queue with this name if it exists, or create it if not.

    queue = aws_connection.lookup(queue_name)

    if queue:
        queue.set_timeout(visibility_timeout)
    else:
        queue = aws_connection.create_queue(queue_name, visibility_timeout)
    
    return queue

class MapCreationQueueMessage(boto.sqs.message.Message):
    def encode(self, value):
        return pickle.dumps(value)

    def decode(self, value):
        return pickle.loads(value)

    def release(self):
        # The message will reappear after the visibility timeout ends.
        # FIXME - should see if there is a quicker way to get it back there.
        pass
    
class AWSMapCreationQueue(object):
    def __init__(self, queue_name, visibility_timeout):
        self.queue = get_or_create_queue(queue_name, visibility_timeout)
        self.queue.set_message_class(MapCreationQueueMessage)

    def get_map_queue_state(self, map_id=None):
        # FIXME - This method will need info from more than just the queue
        # Will probably need to take it off this class.
        
        # This is a stub which returns something to display so that things don't break
        return { 'new': 0, 'working': 0, 'complete': 0, 'error' : 0, 'to_make': 0 }

    def queue_map(self, map_object):
        message = boto.sqs.message.Message()
        
        message_dict = {
            'station_id': map_object.target_station_id, 
            'postcode': map_object.target_postcode, 
            'target_e': map_object.target_e, 
            'target_n': map_object.target_n,
            'direction': map_object.target_direction, 
            'time': map_object.target_time, 
            'limit_time': map_object.target_limit_time, 
            'date': map_object.target_date,
            }
        
        message.set_body(message_dict)
        self.queue.write(message)

        # FIXME - what is this return value used for? Does this need to return
        # anything?
        #return map_id

    def get_map_from_queue(self, server_description):
        return self.queue.read()
