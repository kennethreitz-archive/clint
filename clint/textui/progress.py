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



class dots(object):
    """Progress iterator. Prints a dot for each item being iterated"""

    def __init__(self, it=None, label='', hide=False):
        self.it = it
        self.label = label
        self.hide = hide
        self.count = 0

    def _finish(self):
        STREAM.write('\n')
        STREAM.flush()

    def __exit__(self, exc_type, exc_value, traceback):
        self._finish()

    def __enter__(self):
        return self

    def update(self):
        STREAM.write(DOTS_CHAR)
        sys.stderr.flush()

    def __iter__(self):
        if not self.hide:
            STREAM.write(self.label)

        for item in self.it:
            if not self.hide:
                self.update()

            self.count += 1

            yield item

        self._finish()


class mill(object):
    """Progress iterator. Prints a mill while iterating over the items."""

    def __init__(self, it=None, label='', hide=False, expected_size=None):
        if it is None and expected_size is None:
            raise TypeError("Either an iterator or expected_size are required")

        self.it = it
        self.label = label
        self.hide = hide
        self.expected_size = expected_size
        self.count = len(it) if expected_size is None else expected_size

    def _mill_char(self, _i):
        if _i == self.expected_size:
            return ' '
        else:
            return MILL_CHARS[_i % len(MILL_CHARS)]

    def _show(self, _i):
        if not self.hide:
            STREAM.write(MILL_TEMPLATE % (
                self.label, self._mill_char(_i), _i, self.count))
            STREAM.flush()

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
        if self.count:
            self._show(0)

        for i, item in enumerate(self.it):

            yield item
            self._show(i+1)

        self._finish()
