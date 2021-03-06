#!/usr/bin/env python
# -*- coding: latin-1 -*-
# $Id: parlparse-ids-lords.py,v 1.3 2011-01-24 12:11:30 louise Exp $

# Converts triple of (name, "House of Lords", date) into parlparse person id.
# Reads lines from standard input, each line having the triple hash-separated.
# Outputs the person ids, one per line.

import sys
import os
import traceback

# Check this out from the ukparse project using Subversion:
# svn co https://scm.kforge.net/svn/ukparse/trunk/parlparse
os.chdir("../../../../parlparse/pyscraper")
sys.path.append(".")
sys.path.append("lords")
import re
from resolvelordsnames import lordsList
from resolvemembernames import memberList
from contextexception import ContextException

while 1:
    sys.stdin.flush()
    line = sys.stdin.readline()
    if not line:
        break

    line = line.decode("utf-8")
    name, cons, date_today = line.split("#")

    id = None
    try:
        id = lordsList.GetLordIDfname(name, None, date_today) 
    except ContextException, ce:
        traceback.print_exc()
    if not id:
        print >>sys.stderr, "failed to match lord %s %s" % (name, date_today)
        print ""
    else:
        person_id = memberList.membertoperson(id)
        print person_id
    sys.stdout.flush()

