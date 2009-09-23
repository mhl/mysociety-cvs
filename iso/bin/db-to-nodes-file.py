#!/usr/bin/python
"""
Take location of stations out of database, and make new .nodes file for new C
tile renderer.

Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
Email: francis@mysociety.org; WWW: http://www.mysociety.org/

$Id: db-to-nodes-file.py,v 1.1 2009-09-23 16:32:28 francis Exp $
"""
import os
import sys
sys.path.append('/home/matthew/lib/python')
import struct

sys.path.append("../../pylib")
import mysociety.config
mysociety.config.set_file("../conf/general")

sys.path.append("../pylib")
import coldb
db = coldb.get_cursor()

import geoconvert

dest_file = os.path.join(mysociety.config.get("TMPWORK"), "test.nodes")
dest_handle = open(dest_file, 'w')

db.execute("""SELECT id, X(position_merc), Y(position_merc)
              FROM station
              ORDER BY id
           """)
db_results = db.fetchall()
expected_id = 1
for (id, x, y) in db_results:
    assert id == expected_id  
    expected_id += 1
    print id, x, y

    out_bytes = struct.pack("=dd", x, y)
    assert len(out_bytes) == 16
    dest_handle.seek(id * 16)
    dest_handle.write(out_bytes)

dest_handle.close()


