#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012  Kan-Ru Chen

# Author(s): Kan-Ru Chen <kanru@kanru.info>

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import cairo
import sys

BOX_SIZE = 99

class Engine(object):
    def __init__(self, fontname):
        self.surface = cairo.ImageSurface(cairo.FORMAT_RGB24, BOX_SIZE, BOX_SIZE)
        self.stride = self.surface.get_stride()
        self.data = self.surface.get_data()
        self.length = len(self.data)
        self.ctx = cairo.Context(self.surface)
        self.ctx.select_font_face(fontname)
        self.ctx.set_font_size(BOX_SIZE)

    def scan(self, char):
        # set to white
        self.ctx.set_source_rgb(1, 1, 1)
        # clean canvas
        self.ctx.paint()

        # draw black glyph
        self.ctx.set_source_rgb(0, 0, 0)

        # move the glyph to the center
        (x_bearing, y_bearing, width, height, x_adv, y_adv) = self.ctx.text_extents(char)
        self.ctx.move_to((BOX_SIZE-width)/2-x_bearing, (BOX_SIZE-height)/2-y_bearing)

        # draw glyph
        self.ctx.show_text(char)

        # calc encoding
        # +-----------------+
        # |0    |1    |2    |
        # |     |     |     |
        # |-----+-----+-----|
        # |3    |4    |5    |
        # |     |     |     |
        # |-----+-----+-----|
        # |6    |7    |8    |
        # |     |     |     |
        # +-----------------+
        acc = [0] * 9
        for row in range(0, self.length-self.stride, self.stride):
            for column in range(0, BOX_SIZE*4, 4):
                offset = row+column
                if ord(self.data[offset]) == 0:
                    acc[self.bucket(row, column)] += 1

        acc = self.normalize(acc)
        if acc == [2.0, 1.0, 2.0, 1.0, 0.0, 1.0, 2.0, 1.0, 2.0]:
            return None
        elif acc == [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0]:
            return None
        else:
            return acc

    def bucket(self, row, column):
        row_3 = BOX_SIZE / 3 * self.stride
        row_6 = BOX_SIZE / 3 * 2 * self.stride
        col_1 = BOX_SIZE*4 / 3 * 1
        col_2 = BOX_SIZE*4 / 3 * 2
        bucket = 0
        if row > row_6:
            bucket = 6
        elif row > row_3:
            bucket = 3

        if column > col_2:
            bucket += 2
        elif column > col_1:
            bucket += 1

        return bucket

    def normalize(self, acc):
        acc2 = [0] * len(acc)
        box_pixels = pow(BOX_SIZE / 3, 2)
        for i in range(0, len(acc)):
            acc2[i] = round(acc[i] / float(box_pixels) * 4)

        return acc2

def zh_chars():
    """Generate Chinese character codes
    http://stackoverflow.com/questions/1366068/whats-the-complete-range-for-chinese-characters-in-unicode
    """
    for i in xrange(0x4E00, 0x9FFF+1):
        yield i
    # for i in xrange(0x3400, 0x4DFF+1):
    #     yield i
    # for i in xrange(0x20000, 0x2A6DF+1):
    #     yield i
    # for i in xrange(0xF900, 0xFAFF+1):
    #     yield i
    # for i in xrange(0x2F800, 0x2FA1F+1):
    #     yield i


def font_features(fontname):
    engine = Engine(fontname)
    for char in zh_chars():
        feature = engine.scan(unichr(char))
        if feature:
            yield [feature, char]

def cmp(f1, f2):
    s1 = sum(f1[0])
    s2 = sum(f2[0])
    if s1 < s2:
        return -1
    elif s1 == s2:
        return 0
    else:
        return 1

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: fonts [fontname]"
        sys.exit(1)

    # TODO: sort base on sum of features
    features = []
    for feature in font_features(sys.argv[1]):
        features.append(feature)

    features.sort(cmp)

    print 'fonts = ',
    print features
