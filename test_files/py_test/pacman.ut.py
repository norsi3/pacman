"""
Unit tests for pacman.py
Last Modified: April 29, 2019
"""

import os
import sys
import time
import unittest
from pacman import pacman

class AllTests(unittest.TestCase):
    def test_generic(self):
        self.assertEqual(pacman("generic.txt"), (6, 1, 27))
    def test_tiny(self):
        self.assertEqual(pacman("tinytest.txt"), (1, 4, 7))
    def test_edge(self):
        self.assertEqual(pacman("edge.txt"), (-1, -1, 0))
    def test_runtime(self):
        self.assertEqual(pacman("runtime.txt"), (2142, 147, 148))
    def test_wallstart(self):
        self.assertEqual(pacman("wallstart.txt"), (-1, -1, 0))
    def test_badstart(self):
        self.assertEqual(pacman("badstart.txt"), (-1, -1, 0))
    def test_circles(self):
        self.assertEqual(pacman("circles.txt"), (1, 0, 6))
    def test_trapped(self):
        self.assertEqual(pacman("trapped.txt"), (0, 0, 0))
    def test_onebyone(self):
        self.assertEqual(pacman("onebyone.txt"),(0, 0, 0))
    def test_noboard(self):
        self.assertEqual(pacman("noboard.txt"), (-1, -1, 0))
    def test_emptyfile(self):
        self.assertEqual(pacman("empty.txt"), (-1, -1, 0))
    def test_badinstructions(self):
        self.assertEqual(pacman("badinst.txt"), (-1, -1, 0))
    def test_badwalls(self):
        self.assertEqual(pacman("badwalls.txt"), (-1, -1, 0))
    def test_everysquare(self):
        self.assertEqual(pacman("everysquare.txt"), (0, 0, 24))
                
if __name__ == '__main__':
    for testClass in [AllTests]:
        print('\n\nTest Class: {}\n'.format(testClass.__name__))
        suite = unittest.TestLoader().loadTestsFromTestCase(testClass)
        result = unittest.TextTestRunner(verbosity=0).run(suite)
