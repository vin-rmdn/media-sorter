#!/usr/bin/env python3

# ====== DISCLAIMER:
## AS THIS IS A HEAVY OPERATION, WE ARE USING THE MULTITHREAD LIBRARY.

# ====== TO-DO:
## Implement similarity matrix, with math rules (a == b and b == c -> a == c) sort of stuff

# ====== EXTERNAL LIBRARIES
## Image-related libraries
import imagehash		# average hash
from PIL import Image	# loading images
import cv2				# showing images
## OS-related libraries
import sys				# argv
import os				# check dir
import time				# sleep function
import platform			# File path distinction
import subprocess
## Calculation
import operator
### Multiprocessing - utilise real threads.
from multiprocessing import Process, Value, Array, Pool, Manager, freeze_support
### GPU
#from numba import cuda
## Debugging purposes
from pprint import pprint
from itertools import repeat

# ====== External functions
## User functions
import imageDuplicate

# ====== CONSTANTS
CUTOFF = 1				# Average hash difference cutoff.
THREADS = 8				# de facto threads. 2/3 off threads recommended.
SEPARATOR = '\\' if platform.system() == 'Windows' else '/'
IMAGE_VIEWER = 'C:\\Program Files\\IrfanView\\i_view64.exe'
USE_CUSTOM_IMAGE_VIEWER = True
SUPPORTED_EXTS = ['.jpg', '.jpeg', 'png']

# ====== Global variables
## Integer variables
CURRENT_TASKS = [0] * THREADS
TOTAL_TASKS = 0
TOTAL_TASKS_PER_JOBS = [0] * THREADS
## Database
FILES = None
deleted_files = []

def count_remaining_tasks(num):
	number = 0
	for i in range(1, num + 1):
		number += i - 1
	return number

def resolve_conflict(image1_id, image2_id):
	global FILES, deleted_files
	# Check if file is deleted alr.
	if (FILES[image1_id] in deleted_files) or (FILES[image2_id] in deleted_files):
		print('File deleted already. Moving on.')
		return None
	elif (operator.xor(os.path.basename(FILES[image1_id])[:6] == 'COR - ', os.path.basename(FILES[image2_id])[:6] == 'COR - ')):
		delete_candidate = FILES[image1_id] if os.path.basename(FILES[image1_id])[:6] == 'COR - ' else FILES[image2_id]
		print('Preferring to deletion of the corrupted file. ({})'.format(delete_candidate))
		os.remove(delete_candidate)
		deleted_files.append(delete_candidate) 
		return None
	print('Similar photos detected. (', FILES[image1_id], ', ', FILES[image2_id], ').', sep='', end='')
	while True:
		ch = input('Delete? (s=show, d=delete, default=carry on)')
		if ch == 's':
			if not USE_CUSTOM_IMAGE_VIEWER:
				try:
					image1_image = cv2.imread(FILES[image1_id])
					cv2.imshow('First image', image1_image)
				except:
					print('First image failed to load. Labelling as corrupt.')
				try:
					image2_image = cv2.imread(FILES[image2_id])
					cv2.imshow('Second image', image2_image)
				except:
					print("Second image failed to load. Labelling as corrupt.")
				try:
					cv2.waitKey(0)
					cv2.destroyAllWindows()
				except:
					print('Huh?')
			else:
				subprocess.Popen([IMAGE_VIEWER, FILES[image1_id]])
				subprocess.Popen([IMAGE_VIEWER, FILES[image2_id]])
		elif ch == 'd':
			remove_candidate = imageDuplicate.process_image(FILES[image1_id], FILES[image2_id], False, False)
			if remove_candidate == None:
				break
			print('Deleting', remove_candidate)
			os.remove(remove_candidate)
			deleted_files.append(remove_candidate)
			break
		else:
			break

def label_corrupt(image_id):
	global SEPARATOR, FILES
	filename = os.path.basename(FILES[image_id])
	dirname = os.path.dirname(FILES[image_id]) + SEPARATOR
	if filename[:6] == 'COR - ':
		print('Already labelled.')
	else:
		new_label = dirname + 'COR - ' + filename
		print(FILES[image_id], '->', new_label)
		os.rename(FILES[image_id], new_label)
		FILES[image_id] = new_label

def operation(database, image1_list, image2_list, id, THREADS, CURRENT_TASKS, TOTAL_TASKS_PER_JOBS, JOB_REQUIRES_PRINTING, conflicting_images, corrupt_images):
	# GLOBAL CONSTANTS
	global SUPPORTED_EXTS
	
	# Main loop function
	for i in range(len(image1_list)):
		progress_text = ''
		# Queue up for shared printing.
		while JOB_REQUIRES_PRINTING == 1:
			time.sleep(0.1)

		# Mutually exclusive operation: printing.
		JOB_REQUIRES_PRINTING = True
		CURRENT_TASKS[id] += 1
		for j in range(THREADS):
			progress_text += str(j) + ':' + str(CURRENT_TASKS[j]) + '/' + str(TOTAL_TASKS_PER_JOBS[j])
			if (j != THREADS - 1):
				progress_text += ' '
		print(progress_text, sep='', end='\r')
		JOB_REQUIRES_PRINTING = False

		# Normal jobs
		image1_fullpath = database[image1_list[i]]
		image2_fullpath = database[image2_list[i]]

		# File verification
		if not (os.path.isfile(image1_fullpath) and os.path.isfile(image2_fullpath)):
			if (os.path.isdir(image1_fullpath) or os.path.isdir(image2_fullpath)):
				continue
			not_existing = image1_fullpath if not os.path.isfile(image1_fullpath) else (image2_fullpath if not os.path.isfile(image2_fullpath) else '')
			print(' ' * len(progress_text), end='\r')
			print('File is probably magically corrupted. (', not_existing, '). Moving on.', sep='')
			continue
		elif os.path.splitext(image1_fullpath)[1].lower() not in SUPPORTED_EXTS or os.path.splitext(image2_fullpath)[1].lower() not in SUPPORTED_EXTS:
			continue

		# Image variable initialisation.
		image1_hash = None
		image2_hash = None

		try:
			image1_hash = imagehash.average_hash(Image.open(image1_fullpath))
		except:
			if image1_list[i] in corrupt_images:
				print('.', end='')
			else:
				print(' ' * len(progress_text), end='\r')
				print('NOT A COMPLETE IMAGE:', image1_fullpath)
				corrupt_images.append(image1_list[i])
		
		try:
			image2_hash = imagehash.average_hash(Image.open(image2_fullpath))
		except:
			if image2_list[i] in corrupt_images:
				print('.', end='')
			else:
				print(' ' * len(progress_text), end='\r')
				print('NOT A COMPLETE IMAGE:', image2_fullpath)
				corrupt_images.append(image2_list[i])

		if image1_hash == None or image2_hash == None:
			print(' ' * len(progress_text), end='\r')
			print('Skipping.', end='\r')
			continue
		elif (image1_hash - image2_hash < CUTOFF):
			if [image1_fullpath, image2_fullpath] in conflicting_images:
				print(',', end='')
			else:
				print(' ' * len(progress_text), end='\r')
				print('Conflict found. (', image1_fullpath, image2_fullpath)
				cand_array = [image1_list[i], image2_list[i]]
				conflicting_images.append(cand_array)


	#return return_array


def __main__():
	global THREADS, FILES, LOCATION, CURRENT_TASKS, TOTAL_TASKS, TOTAL_TASKS_PER_JOBS, SEPARATOR, FILES

	# Local variable initialisation
	# Return items
	freeze_support()
	manager = Manager()
	conflicting_images = manager.list()
	corrupt_images = manager.list()

	LOCATION = sys.argv[1]
	if LOCATION[-1] != SEPARATOR:
		LOCATION += SEPARATOR
	FILES = manager.list(os.listdir(LOCATION))

	for i in range(len(FILES)):
		FILES[i] = LOCATION + FILES[i]

	# Something I thought of last night!
	TOTAL_TASKS = count_remaining_tasks(len(FILES))
	image1_queue = [[] for _ in range(THREADS)]
	image2_queue = [[] for _ in range(THREADS)]

	print('Allocating resources.')
	iteration = 0
	for i in range(len(FILES)):
		for j in range(i, len(FILES)):
			if i == j:
				continue
			else:
				#print('Iteration', iteration)
				thread_share = iteration % THREADS
				image1_queue[thread_share].append(i)
				image2_queue[thread_share].append(j)
				iteration += 1
	print('Allocation complete.')

	for i in range(THREADS):
		TOTAL_TASKS_PER_JOBS[i] = len(image1_queue[i])

	# Shared memory allocation: first step.
	CURRENT_TASKS = Array('i', CURRENT_TASKS)
	JOB_REQUIRES_PRINTING = Value('i', 0)
	TOTAL_TASKS_PER_JOBS = Array('i', TOTAL_TASKS_PER_JOBS)

	print('Allocating jobs.')

	jobs = []

	for i in range(0, THREADS):
		thread = Process(target=operation, args=(FILES, image1_queue[i], image2_queue[i], i, THREADS, CURRENT_TASKS, TOTAL_TASKS_PER_JOBS, JOB_REQUIRES_PRINTING, conflicting_images, corrupt_images))
		jobs.append(thread)
	print('Allocation complete once again.')

	for j in jobs:
		j.start()
	
	# Waiting to complete.
	for j in jobs:
		j.join()

	#for i in range(len(FILES)):
	#	for j in range(i, len(FILES)):
	#		if FILES[i] == FILES[j]:
	#			continue
	#		else:
	#			current_tasks += 1
	#			print("Progress: {}/{}".format(current_tasks, total_tasks), end='\r')

	# Aftermission: sort out differences.
	print('====== Info ======')
	print('Conflicting images:', len(conflicting_images))
	print(conflicting_images)
	print('Corrupted images:', len(corrupt_images))
	print(corrupt_images)
	print('==================')

	for i in range(len(corrupt_images)):
		label_corrupt(corrupt_images[i])
	else:
		for i in range(len(conflicting_images)):
			resolve_conflict(conflicting_images[i][0], conflicting_images[i][1])

	print('Completed.')
				


if __name__ == '__main__':
	freeze_support()
	__main__()