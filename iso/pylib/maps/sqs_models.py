
import boto.sqs.connection

import mysociety.config

aws_connection = boto.sqs.connection.SQSConnection(
    mysociety.config.get('AWS_KEY'),
    mysociety.config.get('AWS_SECRET'),
    )

aws_queue_name = mysociety.config.get('AWS_MAP_CREATION_QUEUE_NAME')
aws_visibility_timeout = int(
    mysociety.config.get('AWS_MAP_CREATION_QUEUE_VISIBILITY_TIMEOUT')
    )

def get_or_create_queue(queue_name, visibility_timeout):
    # Get the queue with this name if it exists, or create it if not.

    queue = aws_connection.lookup(queue_name)

    if queue:
        queue.set_timeout(visibility_timeout)
    else:
        queue = aws_connection.create_queue(queue_name, visibility_timeout)
    
    return queue

def get_map_creation_queue():    
    return get_or_create_queue(aws_queue_name, aws_visibility_timeout)
