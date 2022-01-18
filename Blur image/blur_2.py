import cv2
import numpy as np
import sys
from blur_1 import display
from blur_1 import initialize
import time

def numpyblur(src,dst):
    """Blurs image using vectorized operations. src is the padded image,
    dst is the destination image"""
    src = src.astype("uint32")
    dst = dst.astype("uint32")

    #Moves the square to add together through the src image
    dst += (src[0:-2,0:-2,:] + src[0:-2,1:-1,:] + src[0:-2,2:,:]
                + src[1:-1,2:,:] + src[2:,2:,:] + src[2:,1:-1,:]
                + src[1:-1,0:-2,:] + src[2:,:-2,:])
    dst = dst /9
    dst = dst.astype("uint8")
    return dst

if __name__ == "__main__":
    src,dst = initialize(sys.argv[1],1)

    t0 = time.perf_counter()
    dst = numpyblur(src,dst)
    t1 = time.perf_counter()

    #Writes time to file
    # report = open("report2.txt", "w")
    # report.write('{:.3f} sec'.format(t1-t0))
    # report.close()

    display("Blurred",dst)
