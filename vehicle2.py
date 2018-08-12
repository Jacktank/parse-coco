#!/usr/bin/env python
# coding=utf-8

from pycocotools.coco import COCO
import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt
import pylab
import cv2
pylab.rcParams['figure.figsize'] = (8.0, 10.0)

#dataDir='/home/jackstan/workspace/docker-test/coco-train/DL_dataset'
dataDir='/home/jackstan/DL_Database'
dataType=['train2017', 'val2017', 'test2017']
annFile='{}/annotations/instances_{}.json'.format(dataDir, dataType[0])

coco=COCO(annFile)
cats = coco.loadCats(coco.getCatIds())
nms=[cat['name'] for cat in cats]

className = dict()
for cat in cats:
    className[cat['id']] = cat['name']
print className

with open('./classes.txt', 'w') as f:
    f.write('background\n')
    for e in className:
        f.write(className[e] + '\n')
    f.close()

#catIds = coco.getCatIds(catNms=nms)
#
#for catId in catIds:
#    imgIds = coco.getImgIds(catIds=catId)
#    imgs = coco.loadImgs(imgIds=imgIds)
#    print imgIds
#    print type(imgIds)

imgIds = coco.getImgIds()
imgs = coco.loadImgs(ids=imgIds)

i = 0
for img in imgs:
    I = cv2.imread('%s/images/%s/%s'%(dataDir, dataType[0], img['file_name']))
    #print '%s/images/%s/%s'%(dataDir, dataType[0], img['file_name'])
    print I.shape
    print I.shape[:2]
    label_img = np.zeros(I.shape[:2], dtype=np.int8)
    anns = coco.loadAnns(ids = coco.getAnnIds(imgIds = img['id']))
    for an in anns:
        m = coco.annToMask(an)
        label_img += (m * an['category_id'])
    cv2.imshow('output', I)
    cv2.imwrite('%d.png'%i, label_img)
    cv2.imshow('output1', label_img)
    k = cv2.waitKey(0)
    i = i + 1
    if k == 27:
        break

#def main(argv):
#
#
#if __main__ == "__main__":
#    main(sys.argv[1:])
