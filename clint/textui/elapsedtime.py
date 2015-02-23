# -*- coding: utf-8 -*-

"""
clint.textui.elapsedtime
~~~~~~~~~~~~~~~~~

This module provides a simple timer to measure elapsed time.

"""

from __future__ import absolute_import
from threading import Thread

import time
import sys

INDICATOR_TEMPLATE = '%s %s %s\r'
NO_INDICATOR_TEMPLATE = '%s %s\r'

INDICATOR_CHARS = ['|', '/', '-', '\\']

STREAM = sys.stderr


class ElapsedTime(object):
    """Timer class for measuring elapsed time.
    This provides a timer with animation.

    Intended usage:
    with ElapsedTime(*kwargs):
        <code>
    """
    def __enter__(self):
        th = Thread(target=self._print_indicator)
        th.start()
        return self

    def __exit__(self, type_, value, traceback):
        self._done()
        self._running = False
        return False

    def __init__(self, label=None, indicator_chars=INDICATOR_CHARS,
                 interval=0.2, hidden=False):
        self._running = True
        self.label = label
        self.indicator_chars = indicator_chars
        self.interval = interval
        self.hidden = hidden
        self.label = label
        if not self.label:
            self.label = ''
        self._start = time.time()
        self._indicator_index = 0

    def show(self):
        """Write elapsed time to stream, with newline, without indicator."""
        self._write_time(newline=True, show_indicator=False)

    def reset(self):
        """Reset the timer."""
        self._start = time.time()

    def _done(self):
        if not self.hidden:
            self._write_time(newline=True)

    def _show(self):
        if not self.hidden:
            self._write_time()

    def _write_time(self, newline=False, show_indicator=True):
        elapsed = time.time() - self._start
        elapsed_disp = ElapsedTime._format_time(elapsed)
        if not self.indicator_chars or not show_indicator:
            STREAM.write(NO_INDICATOR_TEMPLATE % (
                self.label, elapsed_disp))
            if newline:
                STREAM.write('\n')
            STREAM.flush()
        else:
            STREAM.write(INDICATOR_TEMPLATE % (
                self.label, self.indicator_chars[self._indicator_index],
                elapsed_disp))
            if newline:
                STREAM.write('\n')
            STREAM.flush()
            self._indicator_index = (
                (self._indicator_index+1) % len(self.indicator_chars))

    def _print_indicator(self):
        while self._running:
            self._show()
            time.sleep(self.interval)

    @staticmethod
    def _format_time(seconds):
        time_ = time.gmtime(seconds)
        return time.strftime('%H:%M:%S', time_)
