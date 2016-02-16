#!/usr/bin/env python

"""
Python script to remove entries from ics calendar that don't contain specific pattern
"""

import os.path
import argparse
import re

BEGIN = 'BEGIN:VEVENT'
END = 'END:VEVENT'
PATTERN = 'SUMMARY:.*Solothurn'
EOF = 'END:VCALENDAR'
NEWICS = 'BCS_2.ics'

parser = argparse.ArgumentParser()
parser.add_argument('file', nargs='?', default='basketplan.ics')
args = parser.parse_args()

if os.path.exists(args.file):
    print("converting calendar '%s' to '%s'" % (args.file, NEWICS))
else:
    print("file '%s' does not exist" % args.file)
    quit()

# variables to hold line indices
b = 0
e = 0
p = 0
# add completed events from calendar to list
event = []

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

            # end of event
            if END in line:
                e = i
                # Add event if it contains PATTERN
                if p > b and p < e:
                    new.writelines(event)

                event = []

        # add last line to new file
        new.writelines(EOF)

