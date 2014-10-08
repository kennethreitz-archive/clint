# -*- coding: utf-8 -*-

"""
clint.eng
~~~~~~~~~

This module provides English language string helpers.

"""
from __future__ import print_function


def join(parts, conj='and'):
    parts = parts[:-2] + [u' {} '.format(conj).join(parts[-2:])]
    return u', '.join(parts)


if __name__ == '__main__':
    print(join(['blue', 'red', 'yellow'], conj='or'))
    print(join(['blue', 'red'], conj='or'))
    print(join(['blue', 'red'], conj='and'))
    print(join(['blue'], conj='and'))
    print(join(['blue', 'red', 'yellow', 'green', 'ello'], conj='and'))
