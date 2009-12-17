
import unittest
import time

import models
import aws_storage

import mysociety.config

class TestQueue(unittest.TestCase):
    def testQueueMap(self):
        # Create a map object
        map_obj = models.MapObject(
            target_e = 123456,
            target_n = 345678,
            arrive_by = True,
            target_time = 8*60,
            target_limit_time = 9*60,
            )

        queue = aws_storage.AWSMapCreationQueue(
            mysociety.config.get('AWS_MAP_CREATION_QUEUE_NAME'), 30)
        # Queue it
        queue.queue_map(map_obj)

        # Let's have a look and make sure the message is actually in the queue
        sqs_queue = queue.queue

        time.sleep(30)

        messages = sqs_queue.get_messages()

        passed = 0
        for message in messages:
            if message.get_body() == map_obj.get_identifier():
                passed += 1
                
        assert passed == 1, "Don't worry too much, the message may just not have tured up in the queue in time"

        # And also, check the item is in sdb
        new_map_obj = models.MapObject.objects.get(map_obj.identifier)

        # Check that what we put in is equal to what we got back, and 
        # that it comes back as an int, not, for example, a float.
        assert new_map_obj.target_e == map_obj.target_e
        assert type(new_map_obj.target_e) is int
        assert new_map_obj.target_n == map_obj.target_n
        assert type(new_map_obj.target_n) is int

        # Tidy up
        new_map_obj.delete()
        queue.queue.clear()

#     def testQueueAndFinish(self):
#         # Create a map object
#         map_obj = models.MapObject(
#             target_e = 123456,
#             target_n = 345678,
#             arrive_by = True,
#             target_time = 8*60,
#             target_limit_time = 9*60,
#             )

#         queue = aws_storage.AWSMapCreationQueue('testQueueAndFinish', 30)

#         # Queue it
#         queue.queue_map(map_obj)

#         # Wait a little - this may take a while

#         time.sleep(40)
#         # Now fetch the map back of the queue
#         map_obj2 = queue.get_map_from_queue()

#         map_obj2.mark_as_done('Here it is!')

#         map_obj2.delete()

#         queue.queue.clear()

    def testQueueOneMap(self):
        """Queue one map and leave it on the queue.
        Using this currently so that I can follow with a single
        fastplan run."""
        # Create a map object
        map_obj = models.MapObject(
            target_e = 123456,
            target_n = 345678,
            arrive_by = True,
            target_time = 9*60,
            target_limit_time = 8*60,
            )

        queue = aws_storage.AWSMapCreationQueue(
            mysociety.config.get('AWS_MAP_CREATION_QUEUE_NAME'), 30)
        # Queue it
        queue.queue_map(map_obj)
