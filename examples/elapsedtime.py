#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

sys.path.insert(0, os.path.abspath('..'))

from time import sleep
from clint.textui import elapsedtime


if __name__ == '__main__':
    # Basic use
    with elapsedtime.ElapsedTime():
        sleep(3)

    # Use with options
    with elapsedtime.ElapsedTime(
            label='Running long job...',
            interval=0.1,
            indicator_chars=['o', 'O', '8']):
        sleep(5)

    # Use without indicator
    with elapsedtime.ElapsedTime(
            label='Without indicator:',
            indicator_chars=None):
        sleep(3)

    # Hide the animated timer
    with elapsedtime.ElapsedTime(
            label='Elapsed time:',
            hidden=True) as et:
        for i in range(3):
            print 'This is loop: %d/3' % (i+1)
            sleep(1)
        et.show()

    # Use without 'with' statement
    et = elapsedtime.ElapsedTime(label='Without with:')
    print 'Running long job...'
    sleep(3)
    et.show()
    et.reset()
    print 'Running another long job...'
    sleep(3)
    et.show()
