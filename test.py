#!/usr/bin/env python
# coding=utf-8
import sys
import numpy as np
import cv2

#I = cv2.imread('./cat.jpg')
#cv2.imshow('output', I)
#cv2.waitKey()

def main(argv):
    if 1 == len(argv):
        inputfile = argv[0]
        I = cv2.imread(inputfile)
        cv2.imshow('output', I)
        cv2.waitKey()
        print type(I)
        print I.shape
        print np.unique(I[:, :, 0])
        print np.unique(I[:, :, 1])
        print np.unique(I[:, :, 2])

if __name__ == "__main__":
    main(sys.argv[1:])
