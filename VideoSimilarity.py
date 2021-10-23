import sys
import tools.path
import os

# CONSTANTS

# VARIABLES
DIRECTORY = tools.path.Path(sys.argv[1])

def probe_file(filename):
    file_properties = {}
    # Fills
    file_properties['fullpath'] = filename
    file_properties['filename'], file_properties['extension'] = os.path.splitext(filename)
    
    file_properties['extension'] = file_properties['extension'].lower()

    return file_properties

def main():
    files_properties = []
    for file in os.listdir(DIRECTORY):
        files_properties.append(probe_file(DIRECTORY+file))
    
    #print(files_properties)
    for i in files_properties:
        print(i['filename'])
    

if __name__ == '__main__':
    main()