# -*- coding: utf-8 -*-

"""
clint.textui.progress
~~~~~~~~~~~~~~~~~

This module provides the progressbar functionality.

"""

from __future__ import absolute_import

import os
import sys
import re
import sys
import time

STREAM = sys.stderr

BAR_TEMPLATE = ('\033[0m \033[32m{label}\033[0m |{filled_chars}\033[38;5;240m{empty_chars}\033[0m| '
                '\033[32m{percent}\033[0m{percent_spacer}\033[33m{progress}/{expected_text}{unit_label}\033[0m | '
                '\033[38;5;243m{eta}\033[0m     \r'
                '\033[0m \033[32m{label}\033[0m |{filled_chars}')
MILL_TEMPLATE = '%s %s %i/%i\r'
TIME_FMT_H = 'ETA: %Hh%Mm'
TIME_FMT_M = 'ETA: %Mm%Ss'
TIME_FMT_S = 'ETA: %Ss'

DOTS_CHAR = '.'
BAR_FILLED_CHAR = '█'
BAR_EMPTY_CHAR = '░'
MILL_CHARS = ['|', '/', '-', '\\']

# How long to wait before recalculating the ETA
ETA_INTERVAL = 1
# How many intervals (excluding the current one) to calculate the simple moving
# average
ETA_SMA_WINDOW = 9

# How long to wait before write
TIME_INTERVAL = 0.3

if os.name == 'nt':
    import msvcrt
    import ctypes

    class _CursorInfo(ctypes.Structure):
        _fields_ = [("size", ctypes.c_int),
                    ("visible", ctypes.c_byte)]


class Bar(object):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.done()
        return False  # we're not suppressing exceptions

    def __init__(self, label='', width=32, hide=None, empty_char=BAR_EMPTY_CHAR,
                 filled_char=BAR_FILLED_CHAR, expected_size=None, every=1,
                 show_percent=False, unit='', unit_label=None, custom_format=None, disable_color=False,
                 no_tty_every_percent=None, auto_hide_cursor=True):
        self.label = label
        self.width = width
        self.hide = hide
        self.empty_char = ' ' if disable_color and empty_char == BAR_EMPTY_CHAR else empty_char
        self.filled_char = '#' if disable_color and filled_char == BAR_FILLED_CHAR else filled_char
        self.expected_size = expected_size
        self.expected_text = f'{expected_size:.0f}'
        self.every = every
        self.start = time.time()
        self.ittimes = []
        self.eta = 0
        self.elapsed = 0
        self.next_status = time.time()
        self.etadelta = time.time()
        self.etadisp = self.format_time(self.eta)
        self.last_progress = 0
        self.show_percent = show_percent
        self.template = custom_format if custom_format else BAR_TEMPLATE
        self.unit = unit
        self.unit_label = f' {unit_label}' if unit_label is not None and unit_label.strip() != '' else ''
        self.last_text_bar = ''
        self.next_percent = 0
        self.line_size = 100
        self.no_tty_every_percent = None
        self.auto_hide_cursor = auto_hide_cursor
        self.cursor_hidden = False
        try:
            if (STREAM.isatty()):
                self.isatty = True
            else:
                self.isatty = False
        except AttributeError:  # output does not support isatty()
            self.isatty = False

        # Only show bar in terminals by default (better for piping, logging etc.)
        if hide is None:
            self.hide = not self.isatty

        if not self.isatty and no_tty_every_percent is not None and isinstance(no_tty_every_percent, int):
            self.no_tty_every_percent = no_tty_every_percent

            if self.no_tty_every_percent < 1:
                self.no_tty_every_percent = 1
            elif self.no_tty_every_percent > 100:
                self.no_tty_every_percent = 100

            self.next_percent = self.no_tty_every_percent

        if disable_color:
            self.template = self.escape_ansi(self.template)

        self.template = '\r' + self.template.strip('\r')

        if self.expected_size:
            self.calculate_expected()
            self.show(0)

    def show(self, progress, count=None):
        if count is not None:
            self.expected_size = count
            self.calculate_expected()
        if self.expected_size is None:
            raise Exception("expected_size not initialized")
        self.last_progress = progress
        if self.auto_hide_cursor and not self.cursor_hidden:
            self.hide_cursor()
            self.cursor_hidden = True
        if progress > self.expected_size:
            self.expected_size = progress
        if not self.hide or self.no_tty_every_percent is not None:
            if (time.time() - self.etadelta) > ETA_INTERVAL:
                self.etadelta = time.time()
                self.ittimes = \
                    self.ittimes[-ETA_SMA_WINDOW:] + \
                    [-(self.start - time.time()) / (progress + 1)]
                self.eta = \
                    sum(self.ittimes) / float(len(self.ittimes)) * \
                    (self.expected_size - progress)
                self.etadisp = self.format_time(self.eta)

            tn = time.time()
            if ((
                    (progress % self.every) == 0 and  # True every "every" updates
                    (tn >= self.next_status)          # and verify the time delay (to prevent a lot of screen write)
            ) or (progress == self.expected_size)):  # And when we're done

                self.next_status = (tn + TIME_INTERVAL) if self.no_tty_every_percent is None else 0
                txt = self.get_text_bar(progress)
                if txt != self.last_text_bar:  # write only when we have changes in text
                    self.last_text_bar = txt
                    p = int((progress / self.expected_size) * 100)
                    if not self.hide or ((p % self.no_tty_every_percent) == 0 and p >= self.next_percent):
                        self.next_percent = (
                            0
                            if self.isatty or self.no_tty_every_percent is None or self.no_tty_every_percent <= 0 else
                            (int(p / self.no_tty_every_percent) * self.no_tty_every_percent) + self.no_tty_every_percent
                        )
                        self.write_output(
                            text=txt,
                            stdout=self.hide and self.no_tty_every_percent is not None
                        )

    def get_text_bar(self, progress):
        if not self.hide or self.no_tty_every_percent is not None:
            x = int(self.width * progress / self.expected_size)
            return self.template.format(
                label=self.label,
                filled_chars=self.filled_char * x,
                empty_chars=self.empty_char * (self.width - x),
                progress=self.format_unit(progress, self.unit),
                expected_text=self.expected_text,
                eta=self.etadisp,
                percent=self.format_percent(progress),
                percent_spacer=" | " if self.show_percent else '',
                unit_label=self.unit_label
            )
        return ''

    def done(self):
        self.clear_line(force=True)
        if not self.hide or self.no_tty_every_percent is not None:
            self.elapsed = time.time() - self.start
            # Print completed bar with elapsed time
            x = int(self.width * self.last_progress / self.expected_size)
            self.write_output(
                self.template.format(
                    label=self.label,
                    filled_chars=self.filled_char * x,
                    empty_chars=self.empty_char * (self.width - x),
                    progress=self.format_unit(self.last_progress, self.unit),
                    expected_text=self.expected_text,
                    eta=self.format_time(self.elapsed),
                    percent=self.format_percent(self.last_progress),
                    percent_spacer=" | " if self.show_percent else '',
                    unit_label=self.unit_label
                ),
                new_line=True,
                stdout=self.hide and self.no_tty_every_percent is not None
            )
        if self.auto_hide_cursor and self.cursor_hidden:
            self.show_cursor()

    def clear_line(self, force=False):
        if (not self.hide or force) and self.isatty:
            STREAM.write('\r\033[0m')
            STREAM.flush()
            STREAM.write((' ' * self.line_size))
            STREAM.write('\r\033[0m')
            STREAM.flush()

    # Expose method to permit print a new line (in stdout) without trash chars at screen
    def print_line(self, text=''):
        self.clear_line()
        print(text, flush=True)
        self.write_output(self.get_text_bar(self.last_progress))

    def format_percent(self, progress):
        if not self.show_percent:
            return ''

        p = (progress / self.expected_size) * 100
        return f' {p:.2f}% '

    def calculate_expected(self):
        self.expected_text = self.format_unit(self.expected_size, self.unit)

        num = self.expected_size
        started = False
        for unit in ["zb", "ep", "pb", "tb", "gb", "mb", "kb", "b"]:
            if started:
                num *= 1024.0
                self.unit = unit

            if self.unit.lower() == unit:
                started = True

        self.expected_size = int(num)
        self.line_size = max([
            len(x) for x in self.escape_ansi(self.get_text_bar(self.expected_size)).replace('\n', '\r').split('\r')
        ] + [self.line_size]) + 16

    @classmethod
    def format_time(cls, seconds):
        if seconds > 60 * 60:  # 1 hour
            return time.strftime(TIME_FMT_H, time.gmtime(seconds))
        elif seconds > 60:  # 1 minute
            return time.strftime(TIME_FMT_M, time.gmtime(seconds))
        else:
            return time.strftime(TIME_FMT_S, time.gmtime(seconds))

    @classmethod
    def write_output(cls, text='', new_line=False, stdout=False):
        if stdout:
            sys.stdout.write(text)
            sys.stdout.write('\r\n')
            sys.stdout.flush()
        else:
            STREAM.write(text)
            if new_line:
                STREAM.write('\n')
            STREAM.flush()

    @classmethod
    def format_unit(cls, num=0, unit=''):
        if unit.lower() in ["b", "kb", "mb", "gb", "tb", "pb", "ep", "zb"]:
            return cls.format_bytes_unit(num, start_unit=unit.upper().replace('B', ''))
        else:
            return f"{num:.0f}"

    @classmethod
    def format_bytes_unit(cls, num, suffix="B", start_unit=""):
        started = False
        for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
            if started or start_unit.upper() == unit:
                started = True
                if abs(num) < 1024.0:
                    return f"{num:3.1f}{unit}{suffix}"
                num /= 1024.0
        return f"{num:.1f}{suffix}"

    @classmethod
    def escape_ansi(cls, text=None):
        if text is None:
            return ''

        pattern = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]')
        return pattern.sub('', text)

    @classmethod
    def hide_cursor(cls):
        if os.name == 'nt':
            ci = _CursorInfo()
            handle = ctypes.windll.kernel32.GetStdHandle(-11)
            ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
            ci.visible = False
            ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
        elif os.name == 'posix':
            sys.stdout.write("\033[?25l")
            sys.stdout.flush()

    @classmethod
    def show_cursor(cls):
        if os.name == 'nt':
            ci = _CursorInfo()
            handle = ctypes.windll.kernel32.GetStdHandle(-11)
            ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
            ci.visible = True
            ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
        elif os.name == 'posix':
            sys.stdout.write("\033[?25h")
            sys.stdout.flush()


def bar(it, label='', width=32, hide=None, empty_char=BAR_EMPTY_CHAR,
        filled_char=BAR_FILLED_CHAR, expected_size=None, every=1):
    """Progress iterator. Wrap your iterables with it."""

    count = len(it) if expected_size is None else expected_size

    with Bar(label=label, width=width, hide=hide, empty_char=empty_char,
             filled_char=filled_char, expected_size=count, every=every) \
            as bar:
        for i, item in enumerate(it):
            yield item
            bar.show(i + 1)


def dots(it, label='', hide=None, every=1):
    """Progress iterator. Prints a dot for each item being iterated"""

    count = 0

    if not hide:
        STREAM.write(label)

    for i, item in enumerate(it):
        if not hide:
            if i % every == 0:  # True every "every" updates
                STREAM.write(DOTS_CHAR)
                sys.stderr.flush()

        count += 1

        yield item

    STREAM.write('\n')
    STREAM.flush()


def mill(it, label='', hide=None, expected_size=None, every=1):
    """Progress iterator. Prints a mill while iterating over the items."""

    def _mill_char(_i):
        if _i >= count:
            return ' '
        else:
            return MILL_CHARS[(_i // every) % len(MILL_CHARS)]

    def _show(_i):
        if not hide:
            if ((_i % every) == 0 or  # True every "every" updates
                    (_i == count)):  # And when we're done

                STREAM.write(MILL_TEMPLATE % (
                    label, _mill_char(_i), _i, count))
                STREAM.flush()

    count = len(it) if expected_size is None else expected_size

    if count:
        _show(0)

    for i, item in enumerate(it):
        yield item
        _show(i + 1)

    if not hide:
        STREAM.write('\n')
        STREAM.flush()
