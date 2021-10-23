#!/usr/bin/env python3

# ====== DISCLAIMER:
## AS THIS IS A HEAVY OPERATION, WE ARE USING THE MULTITHREAD LIBRARY.

# ====== TO-DO:
## Implement corrupt stuff.
## Fix image = [i in image if smthsmth] because no corruption is contained and yet FILES is static.

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
import numpy as np
### Multiprocessing - utilise real threads.
from multiprocessing import Process, Value, Array, Pool, Manager, freeze_support
### GPU
import numba
from numba import cuda, jit
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
SUPPORTED_EXTS = ['.jpg', '.jpeg', '.png']
DIRECTORY = sys.argv[1]
TOLERANCE = 1

# ====== Global variables
## Integer variables
CURRENT_TASKS = [0] * THREADS
TOTAL_TASKS = 0
TOTAL_TASKS_PER_JOBS = [0] * THREADS
## Database
FILES = None
deleted_files = []
similarity_matrix = None
## Images (load them here instead of using HDD back to back)
images = []

#def count_image(dir):
#	iteration = 0
#	for
#	ge.open(image_dir))
#	print('Process', i + 1, end='\r')
#	return iteration

# Multiprocess version
def hash(args):
	image_dir, i = args
	if os.path.isdir(image_dir):
		return None
	print(image_dir, end='\r')
	try:
		#image_hash = imagehash.average_hash(Image.open(image_dir))
		image_hash = imagehash.phash(Image.open(image_dir))
	except OSError:
		print('CULPRIT:', image_dir, end='\n\n')
		return 'corrupt'
	except:
		print('Are we all living in a simulation?')
	print(' ' * 15, end='\r')
	print('Process', i + 1, end='\r')
	return image_hash.hash

@cuda.jit
def check_similarity(hashes, similarity_matrix, length):
	global CUTOFF
	# CREDITS TO bunchesofdonald OVER ON imagehash
	# Sorry bud, I have to get your 'hash_distance' code because numba won't accept other library functions:(
	# check it out on https://github.com/bunchesofdonald/imagehash !
	
	## image comparison
	for i in range(length):
		for j in range(i + 1, length):
			#image1_flat = []
			#image2_flat = []
			# WE FLATTEN THEM OURSELVES!
			#for k in range(len(hashes[0])):
			#	image1_flat.append(hashes[i][k])
			#	image2_flat.append(hashes[j][k])

			#image1_flat = hashes[i].reshape(64,).copy()
			#image2_flat = hashes[j].reshape(64,).copy()
			diff = 0

			## hash comparison
			#for k in range(len(image1_flat)):
			#	if image1_flat[k] != image2_flat[k]:
			#		diff += 1
			for k in range(len(hashes[i])):
				for l in range(len(hashes[j])):
					if hashes[i][k][l] != hashes[j][k][l]:
						diff += 1

			if diff < CUTOFF: 
				similarity_matrix[i, j] = True
				similarity_matrix[j, i] = True

def check_similarity_gpuless(hashes, similarity_matrix, length):
	global CUTOFF
	# CREDITS TO bunchesofdonald OVER ON imagehash
	# Sorry bud, I have to get your 'hash_distance' code because numba won't accept other library functions:(
	# check it out on https://github.com/bunchesofdonald/imagehash !
	
	## image comparison
	for i in range(length):
		for j in range(i + 1, length):
			#image1_flat = []
			#image2_flat = []
			# WE FLATTEN THEM OURSELVES!
			#for k in range(len(hashes[0])):
			#	image1_flat.append(hashes[i][k])
			#	image2_flat.append(hashes[j][k])

			#image1_flat = hashes[i].reshape(64,).copy()
			#image2_flat = hashes[j].reshape(64,).copy()
			diff = 0

			## hash comparison
			#for k in range(len(image1_flat)):
			#	if image1_flat[k] != image2_flat[k]:
			#		diff += 1
			for k in range(len(hashes[i])):
				for l in range(len(hashes[i][k])):
					if hashes[i][k][l] != hashes[j][k][l]:
						diff += 1

			if diff == 0: 
				similarity_matrix[i, j] = True
				similarity_matrix[j, i] = True

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
	subprocess.Popen([IMAGE_VIEWER, FILES[image1_id]])
	subprocess.Popen([IMAGE_VIEWER, FILES[image2_id]])
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

def __main__():
	# Load global variables
	global DIRECTORY, TOTAL_TASKS, FILES, images, similarity_matrix

	# Check if path ends in separator, if not then add
	if DIRECTORY[-1] != SEPARATOR:
		DIRECTORY += SEPARATOR

	# Get all files
	FILES = os.listdir(DIRECTORY)

	# Get FILES to refer to the full path
	FILES = [DIRECTORY + i for i in FILES]

	# Get amount of image in file
	TOTAL_TASKS = len(FILES)

	# Allocate dataset variables
	similarity_matrix = np.array([[False] * TOTAL_TASKS] * TOTAL_TASKS)

	print('Total images to process:', TOTAL_TASKS)
	
	# Do hash in multiprocess
	print('Calculating hashes of image...', end=' ')
	starttime = time.time()
	pool = Pool(processes=THREADS)
	args = zip(FILES, range(TOTAL_TASKS))
	images = pool.map(hash, args)

	pool.close()
	endtime = time.time()
	print("Done in {} seconds.".format(endtime - starttime))

	# Cleaning images output
	images = [i for i in images if i is not None and i != 'corrupt']	# clear none

	hash_log = open('hashlog.txt', 'w')
	hash_log.write(str(images))
	hash_log.close()

	print('Sending data to GPU... ', end='')
	images_handle = cuda.to_device(images)
	matrix_handle = cuda.to_device(similarity_matrix)
	print('Doing GPU calculations...', end=' ')
	# thread per block, num of block
	check_similarity[64, 1024](images_handle, matrix_handle, len(images))

	print('Getting data back from GPU (slowpoke!)...')
	matrix_handle.copy_to_host(similarity_matrix)

	print('Done!')

	# Data post-processing
	conflicting_images = np.array(np.where(similarity_matrix == True)).T
	conflicting_images = conflicting_images[conflicting_images[:, 0] < conflicting_images[:, 1]]

	print('====== Info ======')
	print('Conflicting images:', len(conflicting_images))
	print(conflicting_images.tolist())
	# TO-DO
	#print('Corrupted images:', len(corrupt_images))
	#print(corrupt_images)
	print('==================')

	#for i in range(len(corrupt_images)):
	#	label_corrupt(corrupt_images[i])
	#else:
	for i in conflicting_images:
		resolve_conflict(i[0], i[1])

	print('Completed.')
			
if __name__ == '__main__':
	freeze_support()
	__main__()