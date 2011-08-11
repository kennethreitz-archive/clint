# -*- coding: utf-8 -*-

"""
clint.textui.progress
~~~~~~~~~~~~~~~~~

This module provides the progressbar functionality.

"""

from __future__ import absolute_import

import sys

STREAM = sys.stderr

BAR_TEMPLATE = '%s[%s%s] %i/%i\r'

DOTS_CHAR = '.'


def bar(it, label='', width=32, hide=False, bar_empty_char='-', bar_filled_char='='):
    """Progress iterator. Wrap your iterables with it."""

    def _show(_i):
        x = int(width*_i/count)
        if not hide:
            STREAM.write(BAR_TEMPLATE % (
                label, bar_filled_char*x, bar_empty_char*(width-x), _i, count))
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


def dots(it, label='', hide=False):
    """Progress iterator. Prints a dot for each item being iterated"""

    count = 0

    if not hide:
        STREAM.write(label)

    for item in it:
        if not hide:
            STREAM.write(DOTS_CHAR)
            sys.stderr.flush()

        count += 1

        yield item

    STREAM.write('\n')
    STREAM.flush()

