#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

sys.path.insert(0, os.path.abspath('..'))

from clint.textui import prompt, puts, colored, validators

if __name__ == '__main__':
    # Standard non-empty input
    name = prompt.query("What's your name?")

    # Set validators to an empty list for an optional input
    language = prompt.query("Your favorite tool (optional)?", validators=[])

    # Shows a list of options to select from
    inst_options = [{'selector':'1','prompt':'Full','return':'full'},
                    {'selector':'2','prompt':'Partial','return':'partial'},
                    {'selector':'3','prompt':'None','return':'no install'}]
    inst = prompt.options("Full or Partial Install", inst_options)

    # Use a default value and a validator
    path = prompt.query('Installation Path', default='/usr/local/bin/', validators=[validators.PathValidator()])

    puts(colored.blue('Hi {0}. Install {1} {2} to {3}'.format(name, inst, language or 'nothing', path)))

