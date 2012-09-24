#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

sys.path.insert(0, os.path.abspath('..'))

from time import sleep
from random import random
from clint.textui import progress

def assertRaises(f, e, *args, **kwargs):
    try:
        f(*args, **kwargs)
        raise Exception("Should have raised an exception: %s" % str(e))
    except e:
        pass

if __name__ == '__main__':
    assertRaises(progress.bar, TypeError)
    assertRaises(progress.mill, TypeError)

    with progress.bar(expected_size=200) as bar:
        for i in range(200):
            bar.update(i+1)
            sleep(0.05)

    for i in progress.bar(range(100)):
        sleep(random() * 0.2)

    for i in progress.dots(range(100)):
        sleep(random() * 0.2)

    with progress.dots() as bar:
        for i in range(200):
            bar.update()
            sleep(0.05)

    for i in progress.mill(range(100)):
        sleep(random() * 0.2)

    with progress.mill(expected_size=200) as bar:
        for i in range(200):
            bar.update(i+1)
            sleep(0.05)

    # Override the expected_size, for iterables that don't support len()
    D = dict(zip(range(100), range(100)))
    for k, v in progress.bar(D.iteritems(), expected_size=len(D)):
        sleep(random() * 0.2)
