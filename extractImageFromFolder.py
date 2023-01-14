#!/usr/bin/env python3

from sys import argv, platform
import os

DELIMITER = '\\' if platform == 'win32' else '/'

def __main__():
	folders = os.listdir(argv[1])
	for i in folders:
		i_fullpath = argv[1] + DELIMITER + i
		#print(i_fullpath)
		if os.path.isdir(i_fullpath):
			files = os.listdir(i_fullpath)
			for j in files:
				j_fullpath = i_fullpath + DELIMITER + j
				if os.path.isfile(j_fullpath):
					filename = i_fullpath + DELIMITER + j
					filenameNew = argv[1] + DELIMITER + j
					os.rename(filename, filenameNew)
					#print(filename, '->', filenameNew)
				else:
					print('Not a file. Skipping;')
		else:
			print('Not a folder. Skipping;')

__main__()