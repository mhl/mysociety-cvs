#
# common.py: Common functions for mySociety site statistics
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: louise@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: common.py,v 1.1 2009-06-01 18:16:30 louise Exp $
#

from datetime import date, timedelta

def end_of_current_week():
    return date.today() - timedelta(days=1)
    
def start_of_current_week():
    return date.today() - timedelta(days=7)
    
def end_of_previous_week():
    return date.today() - timedelta(days=8)

