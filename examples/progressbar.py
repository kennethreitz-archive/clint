#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

from clint.textui.colored import ColoredString

sys.path.insert(0, os.path.abspath('..'))

from time import sleep
from random import random
from clint.textui import progress


if __name__ == '__main__':
    for i in progress.bar(range(100)):
        sleep(random() * 0.2)

    with progress.Bar(label="Bytes formatted", expected_size=2, unit='Gb', unit_label='Size',
                      show_percent=True, every=1024 * 10) as bar:
        for val in range(0, 2 * 1024 * 1024 * 1024, 1024):
            bar.show(val)

    with progress.Bar(label="nonlinear", expected_size=10) as bar:
        last_val = 0
        for val in (1,2,3,9,10):
            sleep(2 * (val - last_val))
            bar.show(val)
            last_val = val
            if val == 3:
                bar.print_line("Text line printed!")

    for i in progress.dots(range(100)):
        sleep(random() * 0.2)

    for i in progress.mill(range(100)):
        sleep(random() * 0.2)

    # Override the expected_size, for iterables that don't support len()
    D = dict(zip(range(100), range(100)))
    for k, v in progress.bar(D.items(), expected_size=len(D)):
        sleep(random() * 0.2)
