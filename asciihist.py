# -*- coding: utf-8 -*-
"""
This module contains code to generate ascii representations
of statistical objects
"""
from __future__ import division
from numpy import histogram, ceil
__author__="fccoelho"
__date__ ="$12/10/2009 14:25:05$"
__licence__="GPL v3"
__docformat__ = "restructuredtext en"



class Histogram(object):
    """
    Ascii histogram
    """
    def __init__(self, data, bins=10):
        """
        Class constructor
        
        :Parameters:
            - `data`: array like object
        """
        self.data = data
        self.bins = bins
        self.h = histogram(self.data, bins=self.bins)
    def horizontal(self, height=4, character ='|'):
        """Returns a multiline string containing a
        a horizontal histogram representation of self.data

        :Parameters:
            - `height`: Height of the histogram in characters
            - `character`: Character to use

        >>> d = normal(size=1000)
        >>> h = Histogram(d,bins=25)
        >>> print h.horizontal(5,'|')
        106            |||
                      |||||
                      |||||||
                    ||||||||||
                   |||||||||||||
        -3.42                         3.09
        """
        his = """"""
        bars = self.h[0]/max(self.h[0])*height
        for l in reversed(range(1,height+1)):
            line = ""
            if l == height:
                line = '%s '%max(self.h[0]) #histogram top count
            else:
                line = ' '*(len(str(max(self.h[0])))+1) #add leading spaces
            for c in bars:
                if c >= ceil(l):
                    line += character
                else:
                    line += ' '
            line +='\n'
            his += line
        his += '%.2f'%self.h[1][0] + ' '*(self.bins) +'%.2f'%self.h[1][-1] + '\n'
        return his
    def vertical(self,height=20, character ='|'):
        """
        Returns a Multi-line string containing a
        a vertical histogram representation of self.data

        :Parameters:
            - `height`: Height of the histogram in characters
            - `character`: Character to use

        >>> d = normal(size=1000)
        >>> Histogram(d,bins=10)
        >>> print h.vertical(15,'*')
                              236
        -3.42:
        -2.78:
        -2.14: ***
        -1.51: *********
        -0.87: *************
        -0.23: ***************
        0.41 : ***********
        1.04 : ********
        1.68 : *
        2.32 :
        """
        his = """"""
        xl = ['%.2f'%n for n in self.h[1]]
        lxl = [len(l) for l in xl]
        bars = self.h[0]/max(self.h[0])*height
        his += ' '*(max(bars)+2+max(lxl))+'%s\n'%max(self.h[0])
        for i,c in enumerate(bars):
            line = xl[i] +' '*(max(lxl)-lxl[i])+': '+ character*c+'\n'
            his += line
        return his

            

if __name__ == "__main__":
    from numpy.random import normal
    d = normal(size=1000)
    h = Histogram(d,bins=10)
    print h.vertical(15)
    print h.horizontal(5)
