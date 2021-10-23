#!/usr/bin/env python3

# Import libraries
import sys

# VARIABLES
path = []
use_iterative = False
use_prenaming = False
use_naming = False
use_duplicate = False
use_similar = False

# Error printing function
def print_error(error_string):
	raise Exception('Error: ' + error_string + ' Quitting.')

# Main function
def main(argv):
	for i in range(len(argv)):
		# Getting the mode
		if i == 0:
			if argv[i] == 'iterative':
				use_iterative = True
				use_prenaming = True
				use_naming = True
				use_duplicate = True
			elif argv[i] == 'name':
				use_prenaming = True
			elif argv[i] == 'sorting':
				use_naming = True
			elif argv[i] == 'duplicate':
				use_duplicate = True
			elif argv[i] == 'similar':
				use_similar = True
		elif argv[i][0] == '-':
			#somthing
		else:
			# Path validation?
			

			

	
	# Exclusivity resolution
	if use_iterative and use_similar:
		print_error('Iterative and similar is mutually exclusive.')
	elif use_duplicate and use_similar:
		print_error('Duplicate detection and similar image detection is mutually exclusive.')




if __name__ = '__main__':
	main(sys.argv)