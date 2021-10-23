#!/usr/bin/env python3

import os
import exif
import sys
import time
import datetime
from PIL import Image

USE_SKIP = False
USE_BYTE_COMPARISON = False
IS_WRITABLE = False

def process_image(image1_filename, image2_filename, use_skip = False, use_byte_comparison = False):
    # Local variable assignment
    USE_SKIP = use_skip
    USE_BYTE_COMPARISON = use_byte_comparison
    USE_EXIF = True
    IS_WITH_RESOLUTION = True

    image1 = None
    image2 = None
    image1_max = None
    image2_max = None

    try:
        image1 = exif.Image(image1_filename)
        image2 = exif.Image(image2_filename)
    except:
        print('This image does not support EXIF.', end=' ')
        USE_EXIF = False

    # Check if attribute exists
    if USE_EXIF == True and ('pixel_x_dimension' not in image1.list_all() or 'pixel_x_dimension' not in image2.list_all()):
        print('EXIF used but empty variables found.', end=' ')
        USE_EXIF = False

    if USE_EXIF:
        image1_max = image1.pixel_x_dimension if image1.pixel_x_dimension > image1.pixel_y_dimension else image1.pixel_y_dimension
        image2_max = image2.pixel_x_dimension if image2.pixel_x_dimension > image2.pixel_y_dimension else image2.pixel_y_dimension
    else:
        print('Using PIL instead.')
        image1 = Image.open(image1_filename)
        image2 = Image.open(image2_filename)
        image1_max = image1.size[0] if image1.size[0] > image1.size[1] else image1.size[1]
        image2_max = image2.size[0] if image2.size[0] > image2.size[1] else image2.size[1]

    # Assertion check
    if (image1_max == None or image2_max == None):
        IS_WITH_RESOLUTION = False

    if (IS_WITH_RESOLUTION and image1_max > image2_max):
        print('Resolution-wise, the second image is smaller. (' + image2_filename + ')')
        return image2_filename
    elif (IS_WITH_RESOLUTION and image2_max > image1_max):
        print('Resolution-wise, the first image is smaller. (' + image1_filename + ')')
        return image1_filename
    
    image1_size = os.path.getsize(image1_filename)
    image2_size = os.path.getsize(image2_filename)

    if image1_size > image2_size:
        print('Byte-wise,', image1_filename + ' is bigger than ' + image2_filename)
        return image2_filename
    elif image2_size > image1_size:
        print('Byte-wise,', image2_filename + ' is bigger than ' + image1_filename)
        return image1_filename
        
    else:
        # Get EXIF create time.
        image1_exifdate, image2_exifdate = None, None
        if 'datetime_digitized' in dir(image1) and 'datetime_digitized' in dir(image2):
            image1_exifdate = image1.datetime_digitized
            image2_exifdate = image2.datetime_digitized
        elif 'datetime_original' in dir(image1) and 'datetime_original' in dir(image2):
            image1_exifdate = image1.datetime_original
            image2_exifdate = image2.datetime_original
        else:
            date1_create = datetime.datetime.fromtimestamp(os.path.getctime(image1_filename))
            date2_create = datetime.datetime.fromtimestamp(os.path.getctime(image2_filename))
            print(image1_filename, ': ', date1_create, '\n', image2_filename, ': ', date2_create)
            if date1_create < date2_create:
                print(image2_filename, ' has a newer create time.', sep='')
                return image2_filename
            elif date2_create < date1_create:
                print(image1_filename, ' has a newer create time.', sep='')
                return image1_filename
            else:
                print('[', image1_filename, '] Both of these files have the same create time. Deleting the duplicate.', sep='')
                return image2_filename
            print('Why am I here?')
        
        # Process with EXIF photo time
        if (image1_exifdate == None or image2_exifdate == None):
            return_candidate = image1_exifdate if image1_exifdate == None else image2_exifdate
            print('One of these has EXIF data date, and that is not', return_candidate)
            return return_candidate
        else:
            print(image1_exifdate, image2_exifdate)
            if (image1_exifdate < image2_exifdate):
                print('By EXIF date,', image1_filename, 'is earlier.')
                return image2_filename
            elif(image1_exifdate > image2_exifdate):
                print('By EXIF date,', image2_filename, 'is earlier.')
                return image1_filename
            else:
                print('Identical. Deleting either.')
                return image2_filename

        #print('Size and create time is the same. Deleting copy.')
        #remove_candidate = filename_full_2
        #iteration += 1

def __main__():
    global USE_SKIP, USE_BYTE_COMPARISON, IS_WRITABLE
    if 'k' in sys.argv[2]:
        USE_SKIP = True
    if 'b' in sys.argv[2]:
        USE_BYTE_COMPARISON = True
    if 'd' in sys.argv[2]:
        IS_WRITABLE = True

    cwd = sys.argv[1]
    files = os.listdir(cwd)

    print('Program start.')

    for i in files:
        filename_full = cwd + i
        filename, filename_ext = os.path.splitext(filename_full)
        if os.path.isfile(filename_full):
            #print('File exists.')
            iteration = 1
            remove_candidate = ''
            while (iteration < 100):
                filename_full_2 = filename + ' - ' + str(iteration) + filename_ext
                if os.path.isfile(filename_full_2):
                    print('Duplicate detected. (', filename_full, ')')
                    remove_candidate = process_image(filename_full, filename_full_2)
                    iteration += 1
                else:
                    if not remove_candidate == '':
                        if len(sys.argv) == 3:
                            if IS_WRITABLE:
                                print('Deleting ' + remove_candidate)
                                os.remove(remove_candidate)
                            else:
                                print('Script in safety mode. File will not be deleted.')
                    break

        else:
            print(i + ' is not valid. Skipping.')

if __name__ == '__main__':
	__main__()