#!/usr/bin/env python3

import os
from sys import argv
import exif

# SS: 1242x2208

def __main__():
    files = os.listdir(argv[1])
    for i in files:
        iteration = 0
        filename, filename_ext = os.path.splitext(argv[1] + '/' + i)
        fullpath = argv[1] + i
        print(fullpath)
        print(filename_ext)
        if os.path.isdir(fullpath):
            continue
        elif os.path.isfile(fullpath) and (filename_ext.lower() == '.jpg' or filename_ext.lower() == '.jpeg'):
			with open(fullpath, 'rb') as i_file:
                i_image = exif.Image(i_file)
				
			print(dir(i_image))
			#newpath = argv[1] + 'Screenshot\\' + i
            #os.rename(fullpath, )
        else:
            print(i + ' is not an image file! Skipping.')
    print("Done!")

__main__()