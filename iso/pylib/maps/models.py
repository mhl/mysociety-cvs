import datetime
import os.path

import sdb_models
import s3_models

class MapObject(sdb_models.SDBMap):
    message = None
    temp_iso_file = None
    temp_routes_file = None

    def release(self):
        """Mark the map as queued and return it to the queue"""

        # FIXME - It would be good to return the message to the queue
        # straight away so that another thread could pick it up, but
        # for the moment it's OK to do nothing here and just let the
        # visibility timeout expire.

    def get_iso_file_name(self):
        return os.path.basename(self.temp_iso_file)

    def get_routes_file_name(self):
        return os.path.basename(self.temp_routes_file)

    def get_iso_file(self):
        return s3_models.get_by_key(self.get_iso_file_name())

    def mark_as_done(self):
        """Mark the map as finished"""
        self.working_finished = datetime.datetime.now()
        
        try:
            s3_models.store_file(key_name=self.get_iso_file_name(), 
                                 location=self.temp_iso_file,
                                 delete_file=True)
            s3_models.store_file(key_name=self.get_routes_file_name(), 
                                 location=self.temp_routes_file,
                                 delete_file=True)
        except Exception, e:
            self.mark_as_error(failure_message=e.message)
        else:
            self.save()
            self.message.delete()

    def mark_as_error(self, failure_message='RUIN!'):
        """Mark the map in simpledb as causing an error, and drop
        it from the queue."""
        # FIXME - I think it makes sense to set working_finished here.
        # It may be more appropriate to set something else - we'll see.
        self.working_finished = datetime.datetime.now()
        self.failure_message = failure_message
        self.save()

        if self.message:
            self.message.delete()

    def set_queue_message(self, message):
        """Associate a message on a queue with this map object.

        This is so that we can drop the message from the queue, or release
        is back to the queue, etc. 
        """

        self.message = message

