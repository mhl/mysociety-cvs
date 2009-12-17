"""This is for testing and debug purposes. It's going to deal with a single
message from SQS, in order to avoid having the usual isodaemon sitting there
polling away and costing us money :-)"""

from __future__ import with_statement

def main():
    queue = storage.get_map_creation_queue()
    import pdb;pdb.set_trace()
    map_object = queue.get_map_from_queue()
    
    if map_object:
        # start and load a fastplan
        with fastplanwrapper.SingleProcessFastPlan() as fastplan_pipe:
            fastplanwrapper.fastplan_from_map_obj(
                fastplan_pipe, 
                map_object,
                mysociety.config.get('TMPWORK'),
                )

    else:
        print "Nothing in the queue"

if __name__ == '__main__':
    import sys
    sys.path.extend(['../pylib/', '../../pylib/'])

    import mysociety.config

    # FIXME - at some point we probably want to stop using the main
    # config file - this will cause us to take things off the main SQS queue.
    mysociety.config.set_file("../conf/general")

    import fastplanwrapper
    import storage
    
    main()
