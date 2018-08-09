#!/usr/bin/env python
# coding=utf-8

from pycocotools.coco import COCO
import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt
import json
import types
import pylab
pylab.rcParams['figure.figsize'] = (8.0, 10.0)

dataDir='.'
dataType='train2017'
annFile='{}/annotations/instances_{}.json'.format(dataDir,dataType)

with open(annFile, 'r') as f:
    data = json.load(f)

print 'json\'s type:'
print type(data)
print 'json.key:'
for key in data:
    print key

