import re
import datetime
import sys
import os
import signal
import os.path
import subprocess

import mysociety.config
INDEX_LOCATION = mysociety.config.get('ISODAEMON_FASTINDEX')

FASTPLAN_NAME = '../bin/fastplan-coopt'
FP_ARGS = [FASTPLAN_NAME, INDEX_LOCATION]

# Used at the start of each logfile line
def stamp():
    # Simplified temporarily to remove server bit - Duncan (FIXME)
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Write something to logfile
def log(message_string):
    print stamp(), message_string
    sys.stdout.flush()

# Reads data from coopted C++ process, prints and returns it.
# Checks the line begins with check_regexp, and returns (line, match)
def my_readline(pipe, check_regexp = None):
    line = "DEBUG:"
    while re.match("DEBUG:", line):
        line = pipe.stdout.readline().strip()
        if line == '':
            raise Exception("unexpected EOF from C++ process")
        log("     " + line)

    if check_regexp:
        match = re.match(check_regexp, line)
        if not match:
            raise Exception("expected: " + check_regexp + " got:" + line)
        return (line, match)
    else:
        return line

class SingleProcessFastPlan(object):
    def __enter__(self):
        self.pipe = start_fastplan()
        return self.pipe

    def __exit__(self, *args):
        os.kill(self.pipe.pid, signal.SIGINT)

def start_fastplan():
    """This starts """
    pipe = subprocess.Popen(
        FP_ARGS, 
        stdin=subprocess.PIPE, 
        stdout=subprocess.PIPE,
        )
    my_readline(pipe, 'loading took')
    return pipe

def fastplan(pipe,
             outfile,
             outfile_routes,
             target_direction,
             target_time,
             target_limit_time,
             station_text_id,
             target_e,
             target_n,
             ):
    """Minimal python wrapper round binplan, with no checking of arguments.

    p - a pipe
    outfile - a path to a file to write the iso file to.
    outfile_routes - a path to a file to write the routes file to.
    target_direction - one of 'arrive_by' and 'depart_after'
    target_time - an integer minutes after midnight.
    target_limit_time - an integer minutes after midnight.
    station_text_id - FIXME
    target_e - fully numeric OSGB easting as an int.
    target_n - fully numeric OSGB northing as an int.

    Returns a pair of floats: route finding time taken and output time taken.
    """

    # Start by checking some arguments
    if target_direction == 'arrive_by':
        if target_limit_time > target_time:
            raise ValueError(
                '%s target_limit time %s must be less than target_time %s'
                %(target_direction, target_limit_time, target_time))
    elif target_direction == 'depart_after':
        if target_limit_time < target_time:
            raise ValueError(
                '%s target_limit time %s must be greater than target_time %s'
                %(target_direction, target_limit_time, target_time))
    else:
        raise ValueError('target_direction %s not valid' %target_direction)

    # FIXME - there is a lot more to check.

    # cause C++ program to do route finding

    # Note that we in the case where the station_text_id comes as 
    # an empty string, we replace it with a string containing two
    # single quotes, in order that it does appear as an argument.

    pipe.stdin.write("binplan %s %s %s %d %d %s %d %d\n" % (
            outfile, 
            outfile_routes, 
            target_direction, 
            target_time, 
            target_limit_time, 
            station_text_id or "''", 
            target_e, 
            target_n,
            )
                     )
    my_readline(pipe, 'target')

    # wait for it to finish
    (line, match) = my_readline(pipe, 'route finding took: ([0-9.]+) secs')
    route_finding_time_taken = match.groups()[0]

    # also shows binary time taken
    (line, match) = my_readline(pipe, 'binary output took: ([0-9.]+) secs')
    output_time_taken = match.groups()[0]

    return (float(route_finding_time_taken), float(output_time_taken))

def fastplan_from_map_obj(pipe, map_object, output_directory):
    """Takes a pipe to a fastplan and a map object, and
    a directory to output files to, and creates an iso file
    and a routes file in the output directory.
    """

    map_object.temp_iso_file = os.path.join(
        output_directory, '%s.iso' % map_object.identifier)
    map_object.temp_routes_file = os.path.join(
        output_directory, '%s.routes' %map_object.identifier)

    try:
        fastplan(pipe,
                 map_object.temp_iso_file,
                 map_object.temp_routes_file,
                 'arrive_by' if map_object.arrive_by else 'depart_after',
                 map_object.target_time,
                 map_object.target_limit_time,
                 map_object.station_text_id,
                 map_object.target_e,
                 map_object.target_n,
                 )
    except Exception, e:
        map_object.mark_as_error(failure_message=e.message)
    else:
        map_object.mark_as_done()
