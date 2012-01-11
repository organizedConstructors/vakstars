#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import sqlite3
from datetime import date

# TODO: refactor this, it's ugly
if len(sys.argv) > 1:
    if len(sys.argv) > 2:
        startdate = sys.argv[2]
        if len(sys.argv) > 3:
            points = sys.argv[3]
        else:
            points = 0
    else:
        startdate = date.today().isoformat()
        points = 0

    db = sqlite3.connect('vakstars')
    c = db.cursor()

    # Insert a row of data
    c.execute("""insert into profiles(id, name, startdate, points)
            values (NULL, ?, ?, ?)""", (sys.argv[1], startdate, points))

    # Save (commit) the changes
    db.commit()

    # We can also close the cursor if we are done with it
    c.close()
else:
    print("<Név> [<Belépés dátuma> [<Pontok száma>] ]")
