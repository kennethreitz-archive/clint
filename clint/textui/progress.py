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
# Only show bar in terminals by default (better for piping, logging etc.)
try:
    HIDE_DEFAULT = not STREAM.isatty()
except AttributeError:  # output does not support isatty()
    HIDE_DEFAULT = True

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

def bar(it, label='', width=32, hide=HIDE_DEFAULT, empty_char=BAR_EMPTY_CHAR, filled_char=BAR_FILLED_CHAR, expected_size=None, every=1):
    """Progress iterator. Wrap your iterables with it."""

    def _show(_i):
        if (time.time() - bar.etadelta) > ETA_INTERVAL:
            bar.etadelta = time.time()
            bar.ittimes = bar.ittimes[-ETA_SMA_WINDOW:]+[-(bar.start-time.time())/(_i+1)]
            bar.eta = sum(bar.ittimes)/float(len(bar.ittimes)) * (count-_i)
            bar.etadisp = time.strftime('%H:%M:%S', time.gmtime(bar.eta))
        x = int(width*_i/count)
        if not hide:
            if ((_i % every)==0 or         # True every "every" updates
                (_i == count)):            # And when we're done
                STREAM.write(BAR_TEMPLATE % (
                    label, filled_char*x, empty_char*(width-x), _i, count, bar.etadisp))
                STREAM.flush()

    count = len(it) if expected_size is None else expected_size

    bar.start    = time.time()
    bar.ittimes  = []
    bar.eta      = 0
    bar.etadelta = time.time()
    bar.etadisp  = time.strftime('%H:%M:%S', time.gmtime(bar.eta))

    if count:
        _show(0)

    for i, item in enumerate(it):

        yield item
        _show(i+1)

    if not hide:
            STREAM.write('\n')
            STREAM.flush()


def dots(it, label='', hide=HIDE_DEFAULT, every=1):
    """Progress iterator. Prints a dot for each item being iterated"""

    count = 0

    if not hide:
        STREAM.write(label)

    for (i, item) in enumerate(it):
        if not hide:
            if (i % every)==0:         # True every "every" updates
                STREAM.write(DOTS_CHAR)
                sys.stderr.flush()

        count += 1

        yield item

    STREAM.write('\n')
    STREAM.flush()


def mill(it, label='', hide=HIDE_DEFAULT, expected_size=None, every=1):
    """Progress iterator. Prints a mill while iterating over the items."""

    def _mill_char(_i):
        if _i == 100:
            return ' '
        else:
            return MILL_CHARS[_i % len(MILL_CHARS)]

    def _show(_i):
        if not hide:
            if ((_i % every)==0 or         # True every "every" updates
                (_i == count)):            # And when we're done

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
