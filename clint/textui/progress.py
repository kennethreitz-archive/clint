# -*- coding: utf-8 -*-

"""
clint.textui.progress
~~~~~~~~~~~~~~~~~

This module provides the progressbar functionality.

"""

from __future__ import absolute_import

import sys
import time

STREAM = sys.stderr

BAR_TEMPLATE = '%s[%s%s] %i/%i - %s\r'
MILL_TEMPLATE = '%s %s %i/%i\r'  

DOTS_CHAR = '.'
BAR_FILLED_CHAR = '#'
BAR_EMPTY_CHAR = ' '
MILL_CHARS = ['|', '/', '-', '\\']

#How long to wait before recalculating the ETA
ETA_INTERVAL = 1
#How many intervals (excluding the current one) to calculate the simple moving average
ETA_SMA_WINDOW = 9

class bar(object):
    """Progress iterator. Wrap your iterables with it."""

    def _show(self, _i):
        if (time.time() - self.etadelta) > ETA_INTERVAL:
            self.etadelta = time.time()
            self.ittimes = self.ittimes[-ETA_SMA_WINDOW:]+[-(self.start-time.time())/(_i+1)]
            self.eta = sum(self.ittimes)/float(len(self.ittimes)) * (self.count-_i)
            self.etadisp = time.strftime('%H:%M:%S', time.gmtime(self.eta))
        x = int(self.width*_i/self.count)
        if not self.hide:
            STREAM.write(BAR_TEMPLATE % (
            self.label, self.filled_char*x, self.empty_char*(self.width-x), _i, self.count, self.etadisp))
            STREAM.flush()

    def __init__(self, it=None, label='', width=32, hide=False, empty_char=BAR_EMPTY_CHAR, filled_char=BAR_FILLED_CHAR, expected_size=None):
        if it is None and expected_size is None:
            raise TypeError("Either an iterator or expected_size are required")

        self.it = it
        self.label = label
        self.width = width
        self.hide = hide
        self.empty_char = empty_char
        self.filled_char = filled_char
        self.count = len(it) if expected_size is None else expected_size

        self.start    = time.time()
        self.ittimes  = []
        self.eta      = 0
        self.etadelta = time.time()
        self.etadisp  = time.strftime('%H:%M:%S', time.gmtime(self.eta))

        if self.count:
            self._show(0)

    def _finish(self):
        if not self.hide:
            STREAM.write('\n')
            STREAM.flush()

    def __exit__(self, exc_type, exc_value, traceback):
        self._finish()

    def __enter__(self):
        return self

    def update(self, i):
        self._show(i)

    def __iter__(self):
        for i, item in enumerate(self.it):

            yield item
            self._show(i+1)

        self._finish()



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


def mill(it, label='', hide=False, expected_size=None):
    """Progress iterator. Prints a mill while iterating over the items."""

    def _mill_char(_i):
        if _i == 100:
            return ' '
        else:
            return MILL_CHARS[_i % len(MILL_CHARS)]

    def _show(_i):
        if not hide:
            STREAM.write(MILL_TEMPLATE % (
                label, _mill_char(_i), _i, count))
            STREAM.flush()

    count = len(it) if expected_size is None else expected_size

    if count:
        _show(0)

    for i, item in enumerate(it):

        yield item
        _show(i+1)

    if not hide:
        STREAM.write('\n')
        STREAM.flush()
