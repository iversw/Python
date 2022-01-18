import cv2
import numpy as np
import sys
from numba import jit
from blur_1 import initialize
from blur_1 import display
import time


@jit(nopython = True, fastmath = True)
def numbablur(src,dst):
    """Blurs the image in given filename with optimized loops"""
    dims = src.shape

    for h in range(1,dims[0]-1):
        for w in range(1,dims[1]-1):
            for c in range(dims[2]):
                dst[h,w,c] = (src[h,w,c] + src[h-1,w,c]
                 + src[h+1,w,c] + src[h,w-1,c]
                 + src[h,w+1,c] + src[h-1,w-1,c]
                 + src[h-1,w+1,c] + src[h+1,w-1,c]
                 + src[h+1,w+1,c])//9
    return dst

if __name__ == "__main__":

    src, dst = initialize(sys.argv[1],1)
    dst = dst.astype("uint32")
    src = src.astype("uint32")
    t0 = time.perf_counter()
    dst = numbablur(src,dst)
    t1 = time.perf_counter()

    #Writes time to file
    # report = open("report1.txt", "w")
    # report.write('{:.3f} sec'.format(t1-t0))
    # report.close()

    display("Blurred",dst)
