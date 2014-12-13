# -*- coding: utf8 -*-

"""
clint.textui.prompt
~~~~~~~~~~~~~~~~~~~

Module for simple interactive prompts handling

"""

from __future__ import absolute_import, print_function

from .core import puts
from .colored import yellow
from .validators import RegexValidator, YnValidator

try:
    raw_input
except NameError:
    raw_input = input


def yn(prompt, default='y', batch=False):
    # A sanity check against default value
    # If not y/n then y is assumed
    if default not in ['y', 'n']:
        default = 'y'

    def default_prompt(value):
        return '[Y/n]' if value == 'y' else '[y/N]'

    return query(prompt, default=default, validators=[YnValidator()], batch=batch, custom_default_prompt=default_prompt)


def query(prompt, default='', validators=None, batch=False, custom_default_prompt=None):
    # Set the nonempty validator as default
    if validators is None:
        validators = [RegexValidator(r'.+')]

    # Let's build the prompt
    if prompt[-1] is not ' ':
        prompt += ' '

    if default:
        if custom_default_prompt:
            prompt += custom_default_prompt(default)
        else:
            prompt += '[' + default + ']'

    # If input is not valid keep asking
    while True:
        # If batch option is True then auto reply
        # with default input
        if not batch:
            user_input = raw_input(prompt).strip() or default
        else:
            print(prompt)
            user_input = default

        # Validate the user input
        try:
            for validator in validators:
                user_input = validator(user_input)
            return user_input
        except Exception as e:
            puts(yellow(e.message))
