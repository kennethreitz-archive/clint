#! /usr/bin/env python
# -*- coding: utf-8 -*-

from clint import args
from clint.textui import puts, colored

all_args = args.grouped

for item in all_args:
    if item is not '_':
        puts(colored.red("key:%s"%item))
        print(all_args[item].all)

