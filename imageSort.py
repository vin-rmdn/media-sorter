#!/usr/bin/env python3

import os
import io
from sys import argv
import re
from pathlib import Path

import exif
import exifread
from exifread.heic import NoParser
import pyheif

SUPPORTED_EXTS = ['.jpg', '.jpeg', '.png', '.heic']


def rename_file(old_file: Path ,new_file: Path) -> None:
    try:
        print(f"\tNew file: {new_file}", end="")
        os.rename(old_file, new_file)
        print(" - saved")
    except Exception as e:
        print(f"Error while renaming: {e}")


def main():
    path = Path(argv[1]).resolve()
    # files = list(os.walk(path))[0][2]   # ensuring only files get picked up
    files = (x for x in path.iterdir() if x.is_file())

    for file in files:
        # Variables
        iteration = 0
        fullpath = path / file

        # Conditionals
        if file.suffix.lower() not in SUPPORTED_EXTS:
            print(f'File extension ({file.suffix}) not supported. Skipping.')
            continue

        # Debug information
        print(f"Filepath: {file}, extension: {file.suffix}")

        with open(file, 'rb') as f:
            if file.suffix.lower() == '.heic':
                img_heif = pyheif.read_heif(f)
                for metadata in img_heif.metadata or []:
                    if metadata['type'] == 'Exif':
                        img_heif_exif = io.BytesIO(metadata['data'][6:])
                        img_metadata = exifread.process_file(img_heif_exif)
            #     print('Currently HEIF images are not supported. Continuing.')
            #     continue
            else:
                img_metadata = exifread.process_file(f)
        
        img_date = ''
        if 'EXIF DateTimeDigitized' in img_metadata.keys():
            img_date = str(img_metadata.get('EXIF DateTimeDigitized'))
        elif 'EXIF DateTimeOriginal' in img_metadata.keys():
            img_date = str(img_metadata.get('EXIF DateTimeOriginal'))
        else:
            print('Error: EXIF not available.')
            continue
        
        # print(f'\tFile date: {img_date}')
        
        # Renaming
        try:
            img_date_split = re.split('[^0-9]', img_date)
            file_date_str = f"{img_date_split[0]}-{img_date_split[1]}-{img_date_split[2]} - "
            file_date_str += ".".join(img_date_split[3:])
            file_new = path / f"{file_date_str}{file.suffix.lower()}"
        except Exception as e:
            print("Error on date split: ", e)
            continue
            
        # print(f'\tNew file: {file_new}')
        
        if not os.path.isfile(file_new):
            rename_file(file, file_new)
        else:
            iteration = 0
            while True:
                iteration += 1
                file_new_iter = path / f"{file_date_str} - {iteration}{file.suffix.lower()}"
                if not os.path.isfile(file_new_iter) and iteration <= 100:
                    rename_file(file, file_new_iter)
                    break
                elif iteration > 100:
                    print('Error: more than 100 iteration reached. Skipping.')
                    break
        
        # Processing
        # if os.path.isfile(fullpath) and (file.suffix.lower() in supported_exts):
        #     with open(fullpath, 'rb') as i_file:
        #         i_image = exif.Image(i_file)

        #     i_image_date = ''
        #     #print(dir(i_image))
        #     if 'datetime_digitized' in dir(i_image):
        #         try:
        #             i_image_date = i_image.datetime_digitized
        #         except RuntimeWarning:
        #             print('Error in ASCII tag. Skipping.')
        #             continue
        #         print('digitized: ', i_image_date)
        #     elif 'datetime_original' in dir(i_image):
        #         i_image_date = i_image.datetime_original
        #         print('original: ', i_image_date)
        #     else:
        #         print('Date time not available (for now)! Skipping.')
        #         continue
            
        # elif os.path.isfile(fullpath) and (filename_ext.lower() in ['.heic']):
        #     print('HEIC mode.')
        #     with open(fullpath, 'rb') as i_file:
        #         i_image = exifread.process_file(i_file)
        #     i_image_date = ''
        #     #print(i_image.keys())
        #     if 'EXIF DateTimeDigitized' in i_image.keys():
        #         i_image_date = str(i_image.get('EXIF DateTimeDigitized'))
        #         print('digitized:', i_image_date)
        #     elif 'EXIF DateTimeOriginal' in i_image.keys():
        #         i_image_date = str(i_image.get('EXIF DateTimeOriginal'))
        #         print('original:', i_image_date)
        #     else:
        #         print('Date time not available (for now)! Skipping.')
        #         continue

        # else:
        #     print(i + ' is not an image file! Skipping.')
        #     continue

        # i_image_date_split = re.split('[^0-9]', i_image_date)
        # i_image_newdir = argv[1]

        # if argv[1][-1] != '/':
        #     i_image_newdir += '/'

        # for j in range(0, 3):
        #     i_image_newdir += i_image_date_split[j]
        #     if j < 2:
        #         i_image_newdir += '-'
        # i_image_newdir += ' - '
        # for j in range(3, len(i_image_date_split)):
        #     i_image_newdir += i_image_date_split[j]
        #     if j < len(i_image_date_split) - 1:
        #         i_image_newdir += '.'
        # i_image_newdir += filename_ext.lower()
        # if not os.path.isfile(i_image_newdir):
        #     print('New file: ', i_image_newdir)
        #     os.rename(fullpath, i_image_newdir)
        # else:
        #     while True:
        #         iteration += 1
        #         i_image_newdir_iteration = i_image_newdir[:-4] + ' - ' + str(iteration) + filename_ext.lower()
        #         if not os.path.isfile(i_image_newdir_iteration) and iteration <= 100:
        #             print('New file: ', i_image_newdir_iteration)
        #             os.rename(fullpath, i_image_newdir_iteration)
        #             break
        #         elif iteration > 100:
        #             print('Error: more than 100! Skipping.')
        #             break
    print("Done!")
    

if __name__ == '__main__':
    main()
