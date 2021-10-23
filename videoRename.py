#!/usr/bin/env python3

import datetime
from datetime import tzinfo, timezone
from imageSimilarity import SUPPORTED_EXTS
import os
import sys
from hachoir import metadata, parser
import platform
import pytz     # Timezones
import tools.path

# Constants
SUPPORTED_EXTS = ['.mov', '.mp4', '.avi']

# Directory
directory = tools.path.Path(sys.argv[1])

def main():
    files = os.listdir(directory)
    for file in files:
        filename, extension = os.path.splitext(file)
        extension = extension.lower()
        if os.path.isdir(file) or extension not in SUPPORTED_EXTS:
            print(file, 'is not valid. Skipping')
            files.remove(file)
            continue

        attributes = {}

        with parser.createParser(directory+file) as parser_handle:
            metadata_handle = metadata.extractMetadata(parser_handle)
            for i in metadata_handle:
                if i:
                    attributes[i.key] = i.values[0].value

        # Skip if default time.
        if attributes['creation_date'] == datetime.datetime(1904, 1, 1, 0, 0, 0):
            print(file + 'has default date. Skipping.')
            continue

        file_new = str(attributes['creation_date'])+extension
        # Splicing and appending
        file_new = file_new[:10] + ' -' + file_new[10:]
        file_new = file_new.replace(':', '.')  # Maximum Windows compatibility

        if not os.path.isfile(directory+file_new):
            print(file, '->', file_new)
            os.rename(directory+file, directory+file_new)
        else:
            iteration = 1
            file_new_with_extension = os.path.splitext(file_new)[0] + ' - '+str(iteration) + os.path.splitext(file_new)[1]
            while os.path.isfile(directory+file_new_with_extension):
                iteration += 1
                file_new_with_extension = os.path.splitext(file_new)[0] + ' - '+str(iteration) + os.path.splitext(file_new)[1]
            print(file, '->', file_new_with_extension)
            os.rename(directory+file, directory+file_new_with_extension)

if __name__ == '__main__':
    main()