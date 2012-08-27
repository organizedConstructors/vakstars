# -*- coding: utf-8 -*-
"""Unit tests for the database controllers"""
__author__ = 'scorchio'

import unittest
from controllers.db.base import base_controller
from controllers.db.sqlite import sqlite_controller
from controllers.db.mysql import mysql_controller

class TestBaseController(unittest.TestCase):
    def newInstance(self):
        instance = base_controller()

    def test_instantiating(self):
        """Base class should raise an exception when we try to instantiate it."""
        self.assertRaises(base_controller.CannotInstantiate, self.newInstance())

class AbstractDbTest(object):
    def test_null(self):
        pass

class TestSqliteController(unittest.TestCase, AbstractDbTest):
    def setUp(self):
        AbstractDbTest.__init__(self)
        self.sqlite = sqlite_controller.connect('test.sqlite')

class TestMySQLController(unittest.TestCase, AbstractDbTest):
    def __init__(self):
        AbstractDbTest.__init__(self)
        self.mysql = mysql_controller.connect('localhost', 'sqlite_test')
