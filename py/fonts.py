#!/usr/bin/python
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

BOX_SIZE = 99

class Engine(object):
    def __init__(self, fontname):
        self.surface = cairo.Surface(cairo.FORMAT_RGB24, BOX_SIZE, BOX_SIZE)
        self.stride = self.surface.get_stride()
        self.ctx = cairo.Context(self.surface)
        self.ctx.set_font_face(fontname)
        self.ctx.set_font_size(BOX_SIZE)

    def scan(self, char):
        # set to white
        self.ctx.set_source_rgb(1, 1, 1)
        # clean canvas
        self.ctx.paint()

        self.ctx.set_source_rgb(0, 0, 0)
        (_, offset, _, _, _, _) = self.ctx.text_extents(char)
        self.ctx.move_to(0, -offset)
        self.show_text(char)

        buf = self.surface.get_data()
        

def profile_for_font(fontname):
    engine = Engine()
    for char in zh_chars():
        feature = engine.scan(char)
