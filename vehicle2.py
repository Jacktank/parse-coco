#!/usr/bin/env python
# coding=utf-8

from pycocotools.coco import COCO
import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt
import pylab
import cv2
pylab.rcParams['figure.figsize'] = (8.0, 10.0)

dataDir='/home/jackstan/workspace/docker-test/coco-train/DL_dataset'
dataType=['train2017', 'val2017', 'test2017']
annFile='{}/annotations/instances_{}.json'.format(dataDir, dataType[0])

coco=COCO(annFile)
cats = coco.loadCats(coco.getCatIds())
nms=[cat['name'] for cat in cats]
print('COCO categories: \n{}\n'.format(' '.join(nms)))
nms = set([cat['supercategory'] for cat in cats])
print('COCO supercategories: \n{}'.format(' '.join(nms)))

classes = dict[]

print len(cats)


