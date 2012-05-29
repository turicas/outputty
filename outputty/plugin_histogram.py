#!/usr/bin/env python
# coding: utf-8

from __future__ import division
from numpy import histogram, ceil


def write(table, column, orientation='vertical', height=4, character='|',
          bins=5):
    values = zip(*table)[table.headers.index(column)]
    table.histogram = histogram(values, bins)
    his = []
    bars = table.histogram[0] / max(table.histogram[0]) * height
    if orientation == 'vertical':
        for l in reversed(range(1, height + 1)):
            line = ''
            if l == height:
                line = '%s ' % max(table.histogram[0]) #histogram top count
            else:
                line = ' ' * (len(str(max(table.histogram[0]))) + 1) #add leading spaces
            for c in bars:
                if c >= ceil(l):
                    line += character
                else:
                    line += ' '
            his.append(line.rstrip())
        his.append('%.2f%s%.2f' % (table.histogram[1][0], ' ' * bins,
                                   table.histogram[1][-1]))
    else:
        xl = ['%.2f' % n for n in table.histogram[1]]
        lxl = [len(l) for l in xl]
        his.append(' ' * (max(bars) + 2 + max(lxl)) + '%s\n' % \
                   max(table.histogram[0]))
        for i, c in enumerate(bars):
            line = xl[i] + ' ' * (max(lxl) - lxl[i]) + ': ' + character * c
            his.append(line.rstrip())
    return '\n'.join(his)
