#!/usr/bin/env python

"""
Python script to remove entries from ics calendar that don't contain specific pattern.

Calendar for KBBV basketball groups:
https://www.basketplan.ch/exportLeagueHoldingGamesICAL.do?leagueHoldingId=5186
"""

import os.path
import argparse
import re

"""
Lines should be limited to 75 octets (not characters) long. Where a data item is too
long to fit on a single line it can be continued on following lines by starting the
continuation lines with a space character (in hex: 20) or a tab character (in hex: 09).
Therefore reduce pattern to "Solo" to find matchups with long team names.
"""

BEGIN = 'BEGIN:VEVENT'
END = 'END:VEVENT'
PATTERN = 'SUMMARY:.*Solo(\S*)?.([1-3])?'
EOF = 'END:VCALENDAR'
NEWICS = 'BCS_#.ics'

parser = argparse.ArgumentParser()
parser.add_argument('file', nargs='?', default='basketplan.ics')
args = parser.parse_args()

if not os.path.exists(args.file):
    print("file '%s' does not exist" % args.file)
    quit()

# variables to hold line indices
b = 0
e = 0
p = 0
# add completed events from calendar to list
event = []
eventcount = 0

with open(args.file, 'rt') as ics:
    with open(NEWICS, 'wt') as new:
        for i, line in enumerate(ics):
            # begin of event
            if BEGIN in line:
                b = i

            # copy header to new file
            if b == 0:
                new.writelines(line)
            else:
                #print(line)
                event += line

            # find matching pattern as regex
            rgx = re.compile(PATTERN)
            m = rgx.match(line)
            if m is not None:
                p = i
                #print (m.group(0))

                if m.group(2) is not None:
                    OUTFILE = NEWICS.replace('#', m.group(2))

            # end of event
            if END in line:
                e = i
                # Add event if it contains PATTERN
                if p > b and p < e:
                    new.writelines(event)
                    eventcount += 1

                event = []

        # add last line to new file
        new.writelines(EOF)

os.rename(NEWICS, OUTFILE)
print("%d Matches added to calendar -> '%s'" % (eventcount, OUTFILE))
