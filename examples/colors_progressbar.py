#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

sys.path.insert(0, os.path.abspath('..'))

from time import sleep
from random import random
from clint.textui import progress


if __name__ == '__main__':
    for i in progress.bar(range(100),fill_color='blue',empty_char='-',empty_color='yellow',label='progress color',label_color='red'):
        sleep(random() * 0.2)

    for i in progress.dots(range(100),dot_color='red',label='dot color',label_color='green'):
        sleep(random() * 0.2)
    
