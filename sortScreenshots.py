#!/usr/bin/env python3

import os
import sys
import datetime

SEPARATOR = '/'
SUPPORTED_FILES = ['.jpg', '.jpeg', '.png']

def __main__():
    IS_WITH_BYTESIZE = False
    if 'b' in sys.argv[2]:
        IS_WITH_BYTESIZE = True

    location = sys.argv[1]
    if location[-1] != SEPARATOR:
        location += SEPARATOR
    files = os.listdir(sys.argv[1])
    if not files:
        print("Invalid input. Exiting.")
    else:
        for ss in files:
            ext = os.path.splitext(ss)[1].lower()
            if ext not in SUPPORTED_FILES:
                print('File incompatible. Skipped.')
                continue
            ss_fullpath = location + ss
            print(ss_fullpath, ' -> ', sep='', end='')

            if os.path.isdir(ss_fullpath):
                print("Current path is a dir. Skipping.")
            else:
                ss_mod_time_raw = os.path.getmtime(ss_fullpath)
                ss_mod_time = datetime.datetime.fromtimestamp(ss_mod_time_raw)
                ss_c_time_raw = os.path.getctime(ss_fullpath)
                ss_c_time = datetime.datetime.fromtimestamp(ss_c_time_raw)

                ss_time = ss_c_time if ss_c_time < ss_mod_time else ss_mod_time

                # File modification date
                ymd = "%4.i-%2.i-%2.i" % (ss_time.year, ss_time.month, ss_time.day)
                hms = "%2.i-%2.i-%2.i" %  (ss_time.hour, ss_time.minute, ss_time.second)

                # File size
                size = os.path.getsize(ss_fullpath)

                #print(ymd, '-', hms)
                ymd = ymd.replace(" ", "0")
                hms = hms.replace(' ', '0')
                filename_candidate = (ymd + ' - ' + hms + ' - ' + str(size)) if IS_WITH_BYTESIZE else (ymd + ' - ' + hms)
                filename_candidate_full = location + filename_candidate + ext
                if not (os.path.isfile(filename_candidate_full) or os.path.isdir(filename_candidate_full)):
                    print(filename_candidate_full)
                    os.rename(ss_fullpath, filename_candidate_full)
                elif os.path.isfile(filename_candidate_full):
                    iteration = 1
                    filename_candidate_full_with_iteration = location + filename_candidate + ' - ' + str(iteration) + ext
                    while(os.path.isfile(filename_candidate_full_with_iteration)):
                        iteration += 1
                        filename_candidate_full_with_iteration = location + filename_candidate + ' - ' + str(iteration) + ext
                        if iteration == 100:
                            return("Ran for 100 iterations but found none. Exiting.")
                    print(filename_candidate_full_with_iteration)
                    os.rename(ss_fullpath, filename_candidate_full_with_iteration)
                else:
                    print('New path is a folder. Exiting.')
    print('done.')

__main__()