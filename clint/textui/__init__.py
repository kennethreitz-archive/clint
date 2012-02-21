# -*- coding: utf-8 -*-

"""
clint.textui
~~~~~~~~~~~~

This module provides the text output helper system.

"""
import sys
if sys.platform.startswith('win'):
    from ..packages import colorama
    colorama.init()

from . import colored
from . import progress

from .core import *
