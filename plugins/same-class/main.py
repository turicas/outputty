#!/usr/bin/env python

from glob import glob
from base_table import BaseTable


plugins = {}
for plugin_name in glob('plugin_*.py'):
    plugin_name = plugin_name[:-3]
    try:
        plugins[plugin_name] = __import__(plugin_name)
    except ImportError:
        print '*** ERROR: could not import "%s"' % plugin_name
    else:
        print '*** Imported "%s" succesfully' % plugin_name

base_classes = []
for module in plugins.values():
    for object_name in dir(module):
        if 'Table' in object_name and object_name != 'BaseTable':
            base_classes.append(getattr(module, object_name))
Table = type('Table', tuple(base_classes), {})
