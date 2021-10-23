#!/usr/bin/env python3

import os
from sys import argv
import exif
import exifread
import re

supported_exts = ['.jpg', '.jpeg'] # HEIF is special

def __main__():
    files = os.listdir(argv[1])
    for i in files:
        iteration = 0
        filename_ext = os.path.splitext(argv[1] + '/' + i)[1]
        fullpath = argv[1] + i
        print(fullpath)
        print(filename_ext)
        if os.path.isdir(fullpath):
            continue
        elif os.path.isfile(fullpath) and (filename_ext.lower() in supported_exts):
            with open(fullpath, 'rb') as i_file:
                i_image = exif.Image(i_file)

            i_image_date = ''
            #print(dir(i_image))
            if 'datetime_digitized' in dir(i_image):
                i_image_date = i_image.datetime_digitized
                print('digitized: ', i_image_date)
            elif 'datetime_original' in dir(i_image):
                i_image_date = i_image.datetime_original
                print('original: ', i_image_date)
            else:
                print('Date time not available (for now)! Skipping.')
                continue
            
            
        elif os.path.isfile(fullpath) and (filename_ext.lower() in ['.heic']):
            print('HEIC mode.')
            with open(fullpath, 'rb') as i_file:
                i_image = exifread.process_file(i_file)
            i_image_date = ''
            #print(i_image.keys())
            if 'EXIF DateTimeDigitized' in i_image.keys():
                i_image_date = str(i_image.get('EXIF DateTimeDigitized'))
                print('digitized:', i_image_date)
            elif 'EXIF DateTimeOriginal' in i_image.keys():
                i_image_date = str(i_image.get('EXIF DateTimeOriginal'))
                print('original:', i_image_date)
            else:
                print('Date time not available (for now)! Skipping.')
                continue

        else:
            print(i + ' is not an image file! Skipping.')
            continue

        i_image_date_split = re.split('[^0-9]', i_image_date)
        i_image_newdir = argv[1]

        if argv[1][-1] != '/':
            i_image_newdir += '/'

        for j in range(0, 3):
            i_image_newdir += i_image_date_split[j]
            if j < 2:
                i_image_newdir += '-'
        i_image_newdir += ' - '
        for j in range(3, len(i_image_date_split)):
            i_image_newdir += i_image_date_split[j]
            if j < len(i_image_date_split) - 1:
                i_image_newdir += '.'
        i_image_newdir += filename_ext.lower()
        if not os.path.isfile(i_image_newdir):
            print('New file: ', i_image_newdir)
            os.rename(fullpath, i_image_newdir)
        else:
            while True:
                iteration += 1
                i_image_newdir_iteration = i_image_newdir[:-4] + ' - ' + str(iteration) + filename_ext.lower()
                if not os.path.isfile(i_image_newdir_iteration) and iteration <= 100:
                    print('New file: ', i_image_newdir_iteration)
                    os.rename(fullpath, i_image_newdir_iteration)
                    break
                elif iteration > 100:
                    print('Error: more than 100! Skipping.')
                    break
    print("Done!")

__main__()
