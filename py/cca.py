#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (C) Kan-Ru Chen <kanru@kanru.info>
#
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

import random
import img
import sys
import wqy

def binary_search(fonts, block, lo=0, hi=None):
    if hi is None:
        hi = len(fonts)
    val = sum(block)
    while lo < hi:
        mid = (lo+hi)//2
        midval = sum(fonts[mid][0])
        if midval < val:
            lo = mid+1
        elif midval > val:
            hi = mid
        else:
            return mid
    return -1

def find_best_match(fonts, block):
    code = binary_search(fonts, block)
    if code > 0:
        code = code + random.choice(range(0, 3))
        char = unichr(fonts[code][1]).encode('utf-8')
    else:
        char = "　"
    return char

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: cca.py [image]'

    imgpr = img.ImageEncoder()
    imgpr.read(sys.argv[1])

    print '<!doctype><html><head><meta charset=\'utf-8\'/></head><body>'
    print '<pre>'
    for b in imgpr.blocks():
        sys.stdout.write(find_best_match(wqy.fonts, b.pixel()))
        if b.iseol:
            sys.stdout.write('\n')

    # for b in imgpr.blocks():
    #     if any(b.pixel()):
    #         print 1,
    #     else:
    #         print 0,
    #     if b.iseol:
    #         print ''

    print '</pre></body></html>'
