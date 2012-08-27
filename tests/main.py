# -*- coding: utf-8 -*-
"""Unit test coordinator"""
__author__ = 'scorchio'

import unittest

if __name__ == '__main__':
    suite = unittest.TestLoader().discover('.', pattern='*.py', top_level_dir='..') # This should load all the unit tests
    unittest.TextTestRunner(verbosity=2).run(suite)