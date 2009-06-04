#
# common.py: Common functions for mySociety site statistics
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: louise@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: common.py,v 1.2 2009-06-04 13:45:17 louise Exp $
#

from datetime import date, timedelta

def end_of_current_week():
    return date.today() - timedelta(days=1)
    
def start_of_week(end_of_week):
    if (end_of_week == None):
        end_of_week = end_of_current_week()
    return end_of_week - timedelta(days=6)
    
def end_of_previous_week(end_of_week=None):
    if (end_of_week == None):
        end_of_week = end_of_current_week()
    return end_of_week - timedelta(days=7)

def percent_change(current, previous):
    if previous == 0:
        return 'n/a'
    percent_change = (float(current * 100) / float(previous)) - 100
    formatted_percent = "%d%%" % round(percent_change, 0)
    if formatted_percent[0] != '-':
        formatted_percent =  "+%s" % (formatted_percent)
    return formatted_percent