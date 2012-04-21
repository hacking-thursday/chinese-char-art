#!/usr/bin/env python
# -*- encoding=utf8 -*-
#
# Author 2011 Hsin-Yi Chen
import os
import unittest

from py import img as myimg

class UtilsTestCase(unittest.TestCase):

    def setUp(self):
        self.filename = os.path.join('img', 'Lenna.jpg')
        self.imgpr = myimg.ImageEncoder()
        self.imgpr.read(self.filename)

    def test_blocks(self):
        """test transform keyword arguments's name to command's option name.
        """
        blocks = self.imgpr.blocks()
        n_x = 162
        self.assertTrue(blocks[53].iseol)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(UtilsTestCase, 'test'))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
