#!/usr/bin/env python
# coding: utf-8
# title = Reading from CSV and Exporting to HTML
# output = 'nice-software.html'
#You can export your data to HTML using the plugin HTML (that is shipped by
#default with ``outputty``). If you don't specify a filename, the HTML plugin
#will return a string (encoded with ``output_encoding``, specified in
#``Table.__init__``). If it receives the filename, the contents will be saved
#into it and it'll return nothing.

from outputty import Table

my_table = Table()
my_table.read('csv', 'nice-software.csv')
my_table.write('html', 'nice-software.html')
