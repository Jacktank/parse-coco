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
dataType='train2017'
annFile='{}/annotations/instances_{}.json'.format(dataDir,dataType)

coco=COCO(annFile)
cats = coco.loadCats(coco.getCatIds())
nms=[cat['name'] for cat in cats]
print('COCO categories: \n{}\n'.format(' '.join(nms)))
nms = set([cat['supercategory'] for cat in cats])
print('COCO supercategories: \n{}'.format(' '.join(nms)))

#get all images containing given categories, select one at random
#catIds = coco.getCatIds(supNms=['vehicle']);
#catIds = coco.getCatIds(catNms=['bicycle','car','motorcycle','airplane','bus','train','truck','boat']);
catIds = coco.getCatIds(catNms=['bicycle','car','motorcycle','bus','truck']);

for catId in catIds:
    imgIds = coco.getImgIds(catIds=[catId])
    imgs = coco.loadImgs(imgIds)
    for img in imgs:
        I = io.imread('%s/image/%s/%s'%(dataDir, dataType, img['file_name']))
        annIds = coco.getAnnIds(imgIds=img['id'], catIds=catIds)
        anns = coco.loadAnns(annIds)
        #m = coco.annToMask(anns[0])
        #print m.shape
        #for i in range(m.shape[0]):
        #    for j in range(m.shape[1]):
        #        if m[i][j] == 1:
        #            cv2.circle(I, (j, i), 2, (0, 0, 255), 1)       
        
        #pts = anns[0]['segmentation'][0]
        #for idx in range(len(pts) / 2):
        #    cv2.circle(I, (int(pts[2 * idx + 0]), int(pts[2 * idx + 1])), 2, (0, 0, 255), 1)       
        
        #some error in rect, why? 
        rect = anns[0]['bbox']
        cv2.rectangle(I, (int(rect[0]), int(rect[1])), (int(rect[0] + rect[2]), int(rect[1] + rect[3])), (0, 0, 255), -1)       
        plt.imshow(I)
        plt.axis('off')
        #coco.showAnns(anns)
        plt.show()
