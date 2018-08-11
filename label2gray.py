#-*- coding: utf-8 -*-
import sys
import os
import cv2
import shutil
import numpy as np
from PIL import Image

def getpallete(num_cls):
# this function is to get the colormap for visualizing the segmentation mask
    n = num_cls
    pallete = [0] * (n * 3)
    for j in xrange(0, n):
        lab = j
        pallete[j * 3 + 0] = 0
        pallete[j * 3 + 1] = 0
        pallete[j * 3 + 2] = 0
        i = 0
        while (lab > 0):
            pallete[j * 3 + 0] |= (((lab >> 0) & 1) << (7 - i))
            pallete[j * 3 + 1] |= (((lab >> 1) & 1) << (7 - i))
            pallete[j * 3 + 2] |= (((lab >> 2) & 1) << (7 - i))
            i = i + 1
            lab >>= 3
    # return pallete
    mypallete = pallete[0*3:1*3]+pallete[249*3:256*3]+pallete[106*3:109*3]+pallete[77*3:80*3]+pallete[1*3:7*3]
    otherpallete = pallete[7*3:77*3]+pallete[80*3:106*3]+pallete[109*3:249*3]
    return mypallete,otherpallete

def quantizetopalette(silf, palette, dither=False):
    """Convert an RGB or L mode image to use a given P image's palette."""

    silf.load()
    # use palette from reference image
    palette.load()
    if palette.mode != "P":
        raise ValueError("bad mode for palette image")
    if silf.mode != "RGB" and silf.mode != "L":
        raise ValueError("only RGB or L mode images can be quantized to a palette")
    im = silf.im.convert("P", 1 if dither else 0, palette.im)

    # the 0 above means turn OFF dithering
    return silf._new(im)
    # return im

def myquantize(self, colors=256, method=None, kmeans=0, palette=None):
    """
    Convert the image to 'P' mode with the specified number of colors.
    :param colors: The desired number of colors, <= 256
    :param method: 0 = median cut
    1 = maximum coverage
    2 = fast octree
    3 = libimagequant
    :param kmeans: Integer
    :param palette: Quantize to the :py:class:`PIL.ImagingPalette` palette.
    :returns: A new image
    """
    self.load()
    if method is None:
        # defaults:
        method = 0
        if self.mode == 'RGBA':
           method = 2
    if self.mode == 'RGBA' and method not in (2, 3):
        # Caller specified an invalid mode.
        raise ValueError(
                'Fast Octree (method == 2) and libimagequant (method == 3) ' +
                'are the only valid methods for quantizing RGBA images'
                )
    if palette:
        # use palette from
        # reference image
        palette.load()
        if palette.mode != "P":
            raise ValueError("bad mode for palette image")
        if self.mode != "RGB" and self.mode != "L":
            raise ValueError(
                    "only RGB or L mode images can be quantized to a palette"
                    )
        # im = self.im.convert("P", 1, palette.im)
        im = self.im.convert("P", 1 if dither else 0, palette.im)
        # the 0 above means turn OFF dithering
        return self._new(im)
    return self._new(self.im.quantize(colors, method, kmeans))

def run_automatting_file(inputfile,outputfile):
    mypallete,otherpallete = getpallete(256)
    # allpallete = mypallete + otherpallete
    allpallete = mypallete + otherpallete
    if not inputfile.endswith('.png') and not inputfile.endswith('.PNG'):
        return
    print 'process image : ' + inputfile
    img = cv2.imread(inputfile,cv2.IMREAD_UNCHANGED)
    row = img.shape[0]
    col = img.shape[1]
    # img_label = np.zeros((row, col, 1), dtype=np.uint8)
    print 'inputfile shape is ', img.shape
    #alpha = np.zeros((row, col), dtype=np.uint8)
    #alpha[:, :] = img[:, :, 2]
    #img[alpha < 128] = 0
    img_bgr = img[:,:,0:3]
    # Rearrange channels to form BGR
    img_rgb = img_bgr[:,:,::-1]
    pil_im = Image.fromarray(img_rgb)

    palimage = Image.new('P', (16, 16))
    palimage.putpalette(allpallete)

    pil_im_p = quantizetopalette(pil_im, palimage, dither=False)

    cv_im = np.array(pil_im_p)
    cv_im = resizeImage(cv_im,1000,Image.NEAREST)
    # print np.unique(cv_im)
    cv_im_new = cv2.erode(cv_im,None)
    cv_im_new[cv_im_new > 19] = 0
    # print np.unique(cv_im_new)
    cv2.imwrite(outputfile,cv_im_new)

def resizeImage(image,resize_dim,resize_flag):
    # if (resize_flag != Image.NEAREST) or (resize_flag != Image.BILINEAR):
    #   print "resize_flag should = Image.NEAREST or Image.BILINEAR!"
    # retu
    width = image.shape[0]
    height = image.shape[1]
    maxDim = max(width,height)
    # max_resize_dim = 321.0
    max_resize_dim = float(resize_dim)
    if maxDim>max_resize_dim:
        if height>width:
            ratio = float(max_resize_dim/height)
        else:
            ratio = float(max_resize_dim/width)
            # print max_resize_dim,"height=",height,"ratio=",ratio
            image = Image.fromarray(np.uint8(image))
            image = image.resize((int(height*ratio), int(width*ratio)),resample=resize_flag)
            # image = image.resize((300, 450),resample=PILImage.BILINEAR)
            image = np.array(image)
    return image

def main(argv):
    if 1 == len(argv):
        inputfile = argv[0]
        outputfile = "testout.png"
        print 'Input file is "', inputfile
        run_automatting_file(inputfile,outputfile)
    elif 2 == len(argv):
        inputfiledir = argv[0]
        outputfiledir = argv[1]
        print 'Input dir is "', inputfiledir
        print 'Output dir is "', outputfiledir
        for name in sorted(os.listdir(inputfiledir)):
            if not name.endswith('.png') and not name.endswith('.PNG'):
                continue
            # print 'process image : ' + name
            pngpath = inputfiledir + '/' + name
            jpgname = name.split('.')[0] + '.jpg'
            jpgpath = inputfiledir + '/' + jpgname
            if not os.path.isfile (jpgpath):
                print jpgpath, "is not exist!"
                continue
            jpgoutpath = outputfiledir + '/' + jpgname
            shutil.copy (jpgpath, jpgoutpath)
            outpath = outputfiledir + '/' + name
            run_automatting_file(pngpath,outpath)
    else:
        print "format err : please imput: inputfiledir [outputfiledir]"
        return

if __name__ == "__main__":
       main(sys.argv[1:])
