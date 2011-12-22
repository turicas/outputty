#!/usr/bin/env python

_plugins = {}

class Table(object):
    def __init__(self, data=None):
        self.data = data or [5, 4, 3, 2, 1]

    def sort(self):
        self.data.sort()

    def out(self, plugin_name, *args, **kwargs):
        if plugin_name not in _plugins:
            complete_name = 'outputty.plugin_' + plugin_name
            _plugins[plugin_name] = __import__(complete_name,
                                               fromlist=['outputty'])
        _plugins[plugin_name].out(self, *args, **kwargs)
