#!/usr/bin/env python
# coding=utf-8
import sys
import numpy as np
import PIL.Image
import cv2
import scipy
import scipy.io

#img = PIL.Image.open('./cat_json/label.png')
#I = np.array(img, dtype='int8')
#with open('./img.txt', 'w') as f:
#    for i in xrange(I.shape[0]):
#        for j in xrange(I.shape[1]):
#            f.write(str(I[i][j]) + ' ')
#        f.write('\n')
#    f.close
#print I.shape
#
#img_32 = np.array(img, dtype='int32')
#print img_32.shape
#print type(img_32)
#
#cv2.imshow('output', img_32)
#cv2.waitKey()

#p = dict()
#p[2] = 'q1'
#p[1] = 'q2'
#p[3] = 'q3'
#p[4] = 'q4'
#print p
#for e in p:
#    print e
#print len(p)

import os
os.mkdir('../images/label/test')

#def main(argv):
#    if 1 == len(argv):
#        inputfile = argv[0]
#        I = cv2.imread(inputfile)
#        cv2.imshow('output', I)
#        cv2.waitKey()
#        print type(I)
#        print I.shape
#        print np.unique(I[:, :, 0])
#        print np.unique(I[:, :, 1])
#        print np.unique(I[:, :, 2])
#
#if __name__ == "__main__":
#    main(sys.argv[1:])
