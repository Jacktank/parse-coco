#!/usr/bin/env python
# coding=utf-8

from pycocotools.coco import COCO
import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt
import pylab
import os
import cv2
pylab.rcParams['figure.figsize'] = (8.0, 10.0)

dataDir='/home/jackstan/workspace/docker-test/coco-train/DL_dataset'
#dataDir='/home/jackstan/DL_Database'
dataType=['train2017', 'val2017', 'test2017']

type_idx = 0
annFile='{}/annotations/instances_{}.json'.format(dataDir, dataType[type_idx])

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

imgIds = coco.getImgIds()
imgs = coco.loadImgs(ids=imgIds)

f_image_list = open('./image_%s_list.txt'%dataType[type_idx], 'w')
f_label_list = open('./label_%s_list.txt'%dataType[type_idx], 'w')
f_image_label_list = open('./image_label_%s_list.txt'%dataType[type_idx], 'w')

#os.mkdir('%s/images/label'%(dataDir))
#os.mkdir('%s/images/label/%s'%(dataDir, dataType[type_idx]))
i = 0
for img in imgs:
    img_full_name = '%s/images/%s/%s'%(dataDir, dataType[type_idx], img['file_name'])
    I = cv2.imread(img_full_name)
    #print img_name
    label_img = np.zeros(I.shape[:2], dtype=np.int8)
    anns = coco.loadAnns(ids = coco.getAnnIds(imgIds = img['id']))
    for an in anns:
        m = coco.annToMask(an)
        label_img += (m * an['category_id'])
    #cv2.imshow('output', I)
    #cv2.imshow('output1', label_img)
    img_file_name_sub = os.path.splitext(img['file_name'])[0]
    label_full_name = '%s/images/label/%s/%s.png'%(dataDir, dataType[type_idx], img_file_name_sub)
    #i = i + 1
    f_image_list.write(img_full_name + '\n')
    f_label_list.write(label_full_name + '\n')
    f_image_label_list.write(img_full_name + ' ' + label_full_name + '\n')

    #print label_full_name
    cv2.imwrite(label_full_name, label_img)
    #k = cv2.waitKey(0)
    #if k == 27:
    #    break

#def main(argv):
#
#
#if __main__ == "__main__":
#    main(sys.argv[1:])
