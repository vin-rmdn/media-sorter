# Media Sorter — a project by vin-rmdn.

## About

Initially named as imageSortingonDate, the project consists of a manual solution of sorting photos according to their datetime. The idea within the project is that photos (and videos) are manageable if one renames such files to its responding capture date, in which one can then organise their media based on the taken date. This is useful in cases where a database exists that contains unmanaged photos and videos.

This project is made with Python, and uses several external libraries:

* Numba (for CUDA)
* Pillow (for Image representation)
* Imagehash (for image comparisons)
* Numpy (for image array representations)
* Exif, Exifread, and other similar tools
* FFProbe (to read ffmpeg)
* Hachoir (to read image and video metadata better)

Note: this project is initially made with sh, but moved to Python for better library and faster runtime, especially with Numba JIT and CUDA support.

## Mode:

- (iterative) Iterative Duplication Detection
  - Can only be used with naming, sorting, and duplicate resolution.
  - Auto tags all of them.
- (name) Naming
- (sort) Sorting
- (duplicate) Duplicate Resolution
  - Mutually exclusive with: Similar image detection
- (similar) Similar Image Detection, supports input-opt
  - Mutually exclusive with: all

## Wishlists

### Implementation of args:

./imageSortApp.py `<mode>` `<parameter>` `<input>` `<input-opt>`

#### Mode:

- (iterative) Iterative Duplication Detection
  - Can only be used with naming, sorting, and duplicate resolution.
  - Auto tags all of them.
- (name) Naming
- (sort) Sorting
- (duplicate) Duplicate Resolution
  - Mutually exclusive with: Similar image detection
- (similar) Similar Image Detection, supports input-opt
  - Mutually exclusive with: all
