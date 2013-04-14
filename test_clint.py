#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Clint Test Suite."""

import unittest


class ClintTestCase(unittest.TestCase):
    """Clint test cases."""

    def setUp(self):
        import clint


    def tearDown(self):
        pass

class ColoredStringTestCase(unittest.TestCase):
    
    def setUp(self):
        from clint.textui.colored import ColoredString
    
    def tearDown(self):
        pass
    
    def test_split(self):
        from clint.textui.colored import ColoredString
        new_str = ColoredString('red', "hello world")
        output = new_str.split()
        assert output[0].s == "hello"
    
    def test_find(self):
        from clint.textui.colored import ColoredString
        new_str = ColoredString('blue', "hello world")
        output = new_str.find('h')
        self.assertEqual(output, 0)
        
    def test_replace(self):
        from clint.textui.colored import ColoredString
        new_str = ColoredString('green', "hello world")
        output = new_str.replace("world", "universe")
        assert output.s == "hello universe"

if __name__ == '__main__':
    unittest.main()
