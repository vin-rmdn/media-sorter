#!/usr/bin/env python3

import os
import logging
from sys import argv
import exif
import re

SUPPORTED_FILES = ['.mov', '.mp4']

def main():
    if argv[2] == '':
        print('Error: number not inserted. Exiting.')
        return 0
    files = os.listdir(argv[1])
    iteration = int(argv[2])
    for i in files:
        filename, filename_ext = os.path.splitext(argv[1] + '/' + i)
        fullpath = argv[1] + i
        print('Input\t: ', fullpath)
        if os.path.isdir(fullpath):
            continue
        elif os.path.isfile(fullpath) and (filename_ext.lower() in SUPPORTED_FILES):
            #with open(fullpath, 'rb') as i_file:
            #    i_image = exif.Image(i_file)

            i_image_newdir = argv[1]
            if argv[1][-1] != '/':
                i_image_newdir += '/'

            while True:
                i_image_newdir_iteration = i_image_newdir + str(iteration) + filename_ext.lower()
                if not os.path.isfile(i_image_newdir_iteration):
                    print('New file: ', i_image_newdir_iteration)
                    os.rename(fullpath, i_image_newdir_iteration)
                    break
                else:
                    iteration += 1
        else:
            print(i + ' is not an image file! Skipping.')
    print("Done!")

if __name__ == '__main__':
    logging.info('Argv count: %d', len(argv))
    main()
