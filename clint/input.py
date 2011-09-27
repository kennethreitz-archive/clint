# -*- coding: utf-8 -*-

"""
clint.input
~~~~~~~~~~~

This module contains the helper functions for dealing with user input.

"""

from __future__ import absolute_import
from __future__ import with_statement

"""

This function is for custom user input. The prompt arg is a string the user will see. 
The options arg is a dictionary of options as strings and the function to call if the options are input. 
For example,

options = {
    'm'   : male_input,   # if 'm' is input, male_input() will be called
    'f' : female_input    # if 'f' is input, female_input() will be called
}

clint.choose('Enter your gender', **options)

"""
def choose(prompt, **options):
    input = raw_input(prompt + ' ' + str([x for x in options]).replace(', ', '/').replace('\'', '') + ':')
    keys = options.keys()
    for x in range(0, len(keys)):
        if input.lower() == keys[x]:
            options[keys[x]]()
            break

"""

This function is for standard y/n input. If y is input, it returns True. Otherwise, it returns False.

"""    
def yn():
    input = raw_input("Are you sure? [y/n]:")
    if input.lower() == 'y': return True
    else: return False
