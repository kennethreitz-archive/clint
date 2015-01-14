#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
tests.test_resources
~~~~~~~~~~~~~~~

Unit Tests for clint.resources
Files should be written to a temporary directory, not the actual user's settings directory,
to prevent destroying any actual files.

"""

import unittest
import os
from shutil import rmtree
import tempfile

from clint import resources


class TestResources(unittest.TestCase):
    def setUp(self):
        """ Create temporary working directory. Default is something like /tmp/tmpyqbvojuh. Redirect
        resources paths there instead of the user's actual config directory """
        self.temp_dir = tempfile.mkdtemp()

        # Since the directory changes for each test, make sure that the module knows it does not exist.
        # This replaces the resources.init() function
        resources.user._exists = False
        resources.user.path = os.path.join(self.temp_dir, 'user')
        resources.site._exists = False
        resources.site.path = os.path.join(self.temp_dir, 'site')
        resources.cache._exists = False
        resources.cache.path = os.path.join(self.temp_dir, 'cache')
        resources.log._exists = False
        resources.log.path = os.path.join(self.temp_dir, 'log')

    def test_read_write(self):
        """ Write a file to the user path, make sure it exists and the contents match """
        resources.user.write('test.txt', 'test\n')
        self.assertTrue(os.path.isfile(os.path.join(self.temp_dir, 'user', 'test.txt')))
        self.assertEqual('test\n', resources.user.read('test.txt'))

    def test_sub(self):
        """ Check that the AppDir object returned has the appropriate subdirectory """
        sub = resources.user.sub('test_subdir')
        self.assertEqual(os.path.join(self.temp_dir, 'user', 'test_subdir'), sub.path)

    def test_append(self):
        """ Tests writing and appending to a file """
        resources.user.write('test.txt', 'aaaa')
        resources.user.append('test.txt', 'bbbb')
        self.assertEqual('aaaabbbb', resources.user.read('test.txt'))

    def test_delete(self):
        """ Test deleting a file """
        resources.user.write('test.txt', 'abcd')
        resources.user.delete('test.txt')
        self.assertFalse(os.path.exists(os.path.join(self.temp_dir, 'user', 'test.txt')))

    def test_appdir_not_configured(self):
        """ Test that the appdir object raises an exception if it is run before it is configured """
        with self.assertRaises(resources.NotConfigured):
            a = resources.AppDir()
            a.read('test.txt')

    def tearDown(self):
        """ Clean up temporary directory """
        rmtree(self.temp_dir)


if __name__ == '__main__':
    unittest.main()