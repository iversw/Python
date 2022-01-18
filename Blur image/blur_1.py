import cv2
import numpy as np
import sys
import time

def pyblur(src, dst):
    """Blurs the image in given filename using python for loops
    returns the blurred array."""
    dims = src.shape #Finds dimensions of 3d array

    for h in range(1, dims[0] -2):
        for w in range(1, dims[1] -2):
            for c in range(dims[2]):
                dst[h,w,c] = (int(src[h,w,c]) + int(src[h-1,w,c])
                 + int(src[h+1,w,c]) + int(src[h,w-1,c])
                 + int(src[h,w+1,c]) + int(src[h-1,w-1,c])
                 + int(src[h-1,w+1,c]) + int(src[h+1,w-1,c])
                 + int(src[h+1,w+1,c]))/9
    return dst

def display(name,dst):
    """Displays the blurred image"""
    cv2.imshow(name,dst)
    cv2.waitKey()

def save(name, dst):
    """Saves the blurred image with given name as filename"""
    cv2.imwrite(name, dst)

def initialize(filename,resize):
    """Gets values the blur function will calculate. Returns source array
    and destination array"""
    src = cv2.imread(filename)
    src = cv2.resize(src, (0,0), fx = resize, fy=resize)
    dst = np.copy(src)
    src = np.pad(src,((1,1),(1,1),(0,0)), mode = "edge")
    return src, dst

if __name__ == "__main__":
    """Run with filename as argument 1 to display blurred image"""
    src,dst = initialize(sys.argv[1],1)
    dims = src.shape

    t0 = time.perf_counter() #Time only used when section below is not commented
    dst = pyblur(src,dst)
    t1 = time.perf_counter()

    #Writes time and dimensions to file
    # report = open("report1.txt", "w")
    # report.write("Dimensions" +  str(dims))
    # report.write("\n")
    # report.write('{:.3f} sec'.format(t1-t0))
    # report.close()

    display("Blurred",dst)
