#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
tests.test_ColoredString
~~~~~~~~~~~~~~~

Unit Tests for clint.textui.colored

"""

import unittest
import os

from clint.textui.colored import ColoredString


class ColoredStringTestCase(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_split(self):
        new_str = ColoredString('red', "hello world")
        output = new_str.split()
        assert output[0].s == "hello"
    
    def test_find(self):
        new_str = ColoredString('blue', "hello world")
        output = new_str.find('h')
        self.assertEqual(output, 0)
        
    def test_replace(self):
        new_str = ColoredString('green', "hello world")
        output = new_str.replace("world", "universe")
        assert output.s == "hello universe"

    def test_py2_bytes_not_mangled(self):
        # On python 2 make sure the same bytes come out as went in
        new_str = ColoredString('RED', '\xe4')
        assert '\xe4' in str(new_str)
        from clint.textui import puts
        puts(new_str)

    def test_clint_force_color_env_var(self):
        os.environ['CLINT_FORCE_COLOR'] = "1"
        new_str = ColoredString('RED', 'hello world')
        assert new_str.always_color is True


if __name__ == '__main__':
    unittest.main()