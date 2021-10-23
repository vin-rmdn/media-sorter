#!/usr/bin/env python3

from ffprobe import FFProbe
import sys
import os
from pprint import pprint
import re

# Constants
location = sys.argv[1]
regex = re.compile("'creation_time': '[0-9-]*'")
SUPPORTED_EXTS = ['.mp4', '.avi', '.mov']

files = os.listdir(location)

for i in files:
    print(i, end='')
    i_ext = os.path.splitext(i)[1].lower()
    i_full = location + i

    if os.path.isfile(i_full) and i_ext in SUPPORTED_EXTS:
        iteration = 1

        creation_time = 'Not found.'
        try:
            creation_time = FFProbe(i_full).metadata['creation_time']
        except:
            print(' (FFProbe failed. Skipping.)')
            continue
        filenameCandidate = 'unnamed'

        filenameDate = creation_time[:10]
        filenameHour = creation_time[11:19].replace(':', '.')

        filenameCandidate = filenameDate + ' - ' + filenameHour
        filenameExtension = i_ext
        filename = filenameCandidate
        print(' -> ', filename, filenameExtension, sep='')
        filename = location + filename
        print(filename)
        if os.path.isfile(filename + filenameExtension):
            while os.path.isfile(filename + ' (' + str(iteration) + ')' + filenameExtension):
                iteration += 1
            os.rename(i_full, filename + ' (' + str(iteration) + ')' + filenameExtension)
        else:
            os.rename(i_full, filename + filenameExtension)
    elif os.path.isdir(i_full):
        print('is a directory. Skipping')
