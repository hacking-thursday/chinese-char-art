#!/usr/bin/env python
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf8 -*-
#
# Author 2012 Hsin-Yi Chen
import Image
import ImageFilter

def split_img(img, n):
        ret = []
        n_x = img.size[0] / n
        n_y = img.size[1] / n
        dbg('n of x: {0}, y: {1}'.format(n_x, n_y))

        # left is x
        # upper is y
        upper = 0
        for i in range(0, n_y):
            left = 0
            for j in range(0, n_x):
                box = (left, upper, left+n, upper+n)
                #dbg('{}, {}, {}, {}'.format(left, upper, left+n, upper+n))
                region = img.crop(box)
                chrpix = ChrPixel(region)
                if j == n_x -1:
                    chrpix.iseol = True
                ret.append(chrpix)
                left += n
            upper += n
        return ret

def dbg(msg):
    print msg

class ChrPixel(object):

    def __init__(self, img):
        # split to 9 pixel
        self._img = img
        self.iseol = False

    def pixel(self):
        ret = []
        for x in range(0,3):
            for y in range(0,3):
                encn = self.enc(self._img.getpixel((x,y)))
                ret.append(encn)
        return ret

    def enc(self, pix):
        # black: 1
        lv_id = 0
        while pix > 0:
            pix = pix / 4
            lv_id += 1
        return lv_id

class ImageEncoder(object):

    def __init__(self, font_size=3):
        self.font_size = font_size

    def read(self, fname, only_blackwhite=False):
        # covert to gray
        self._img = Image.open(fname).convert('L')
        dbg('SIZE: {0}x{1}, BOXS: {2}'.format(self._img.size[0],
                                           self._img.size[1],
                                           self._img.getbbox()))

        # for each pixel, if pixel > 150: white
        # else: black
        if only_blackwhite:
            for i in range(self._img.size[0]):
                for j in range(self._img.size[1]):
                    # 1 level  is 62
                    if self._img.getpixel((i,j)) > 124:
                        rgb = 255
                    else:
                        rgb = 0
                    self._img.putpixel((i,j), rgb)

    def blocks(self):
        # split to block by font size
        # n is pixels is included in a block
        # left is x
        # upper is y
        return split_img(self._img, self.font_size)
