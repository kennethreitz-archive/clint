# -*- coding: utf-8 -*-

"""
clint.textui.progress
~~~~~~~~~~~~~~~~~

This module provides the progressbar functionality.

"""

from __future__ import absolute_import

from . import colored
import sys

STREAM = sys.stderr

BAR_TEMPLATE = '%s[%s%s] %i/%i\r'

DOTS_CHAR = '.'
BAR_FILLED_CHAR = '#'
BAR_EMPTY_CHAR = ' '

def progress_color(string,color):
    if color is None:
        return string
    else:
        try:
            return str(getattr(colored,color)(string))
        except:
            return string

def bar(it, label='', width=32, hide=False, empty_char=BAR_EMPTY_CHAR, filled_char=BAR_FILLED_CHAR,fill_color=None,empty_color=None,label_color=None):
    """Progress iterator. Wrap your iterables with it."""

    def _show(_i):
        x = int(width*_i/count)
        if not hide:
            STREAM.write(BAR_TEMPLATE % (
                progress_color(label,label_color), progress_color(filled_char*x,fill_color), progress_color(empty_char*(width-x),empty_color), _i, count))
            STREAM.flush()

    count = len(it)

    if count:
        _show(0)

    for i, item in enumerate(it):

        yield item
        _show(i+1)

    if not hide:
        STREAM.write('\n')
        STREAM.flush()


def dots(it, label='', hide=False, dot_color=None, label_color=None):
    """Progress iterator. Prints a dot for each item being iterated"""

    count = 0

    if not hide:
        STREAM.write(progress_color(label,label_color))

    for item in it:
        if not hide:
            STREAM.write(progress_color(DOTS_CHAR,dot_color))
            sys.stderr.flush()

        count += 1

        yield item

    STREAM.write('\n')
    STREAM.flush()

