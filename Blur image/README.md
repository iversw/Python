# Image blurring

## Requirements:

Numpy

Numba

cv2

## Notes:
Scripts to blur images in three different methods / degrees of efficiency. The image is blurred by changing a pixel's color value to the average value of its neighbors' colors.

One uses simple Python for-loops, the other uses numpy matrix multiplication, the third uses numba to speed up the simple Python for-loops.
Blur.py is the main file to run, as it is the most user-friendly, and allows to choose which method to use.
