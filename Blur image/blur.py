import argparse
import cv2
import numpy as np
from blur_1 import pyblur
from blur_1 import initialize
from blur_1 import display
from blur_1 import save
from blur_2 import numpyblur
from blur_3 import numbablur

parser = argparse.ArgumentParser(description = "Blurs the image in the file. "
                                + "\nThe script supports the following arguments:")
required = parser.add_argument_group("required arguments")
required.add_argument("-v", "--version", type = int,metavar="",required=True,
                    help = "Determines which function to use. 1-3 are valid inputs")
required.add_argument("-f", "--filename", required = True, metavar = "",
                    help = "Filename of the image you want to blur")
parser.add_argument("-r", "--resize",type=float, metavar="",
                    help = "Call to resize the output image. For instance:" +
                    " 0.5 to get half of the original dimensions")
required.add_argument("-n", "--newfile", metavar="", help = "Name of output file")

group = parser.add_argument_group("save or display required")
group = group.add_mutually_exclusive_group()
group.add_argument("-s", "--save", action = "store_true",
                    help = "Call with -s flag to save image")
group.add_argument("-d","--display", action = "store_true",
                    help = "Call with -d flag to display image")
args = parser.parse_args()

if args.resize:
    src,dst = initialize(args.filename,args.resize)
else:
    src,dst = initialize(args.filename,1)

if args.version not in [1,2,3]:
    print("Only 1,2 or 3 are valid version inputs")

if args.version == 1:
    if args.display:
        display(args.newfile,pyblur(src,dst))
    if args.save:
        save(args.newfile, pyblur(src,dst))

if args.version == 2:
    if args.display:
        display(args.newfile,numpyblur(src,dst))
    if args.save:
        save(args.newfile, numpyblur(src,dst))

if args.version == 3:
    if args.display:
        src = src.astype("uint32")
        dst = dst.astype("uint32")
        display(numbablur(src,dst))
    if args.save:
        save(args.newfile, numbablur(src,dst))
